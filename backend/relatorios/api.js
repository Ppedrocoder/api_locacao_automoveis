const express = require("express");
const soap = require("soap");
const http = require("http");
const path = require("path");
const fs = require("fs");
const { WebSocketServer, WebSocket } = require("ws");

const app    = express();
const server = http.createServer(app);

app.use(express.json());

app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");

    if (req.method === "OPTIONS") {
        return res.sendStatus(204);
    }

    next();
});

// ── WebSocket ─────────────────────────────────────────
const wss = new WebSocketServer({ server });
const clientes = new Set();
let ultimoSnapshot = null;

wss.on("connection", (ws) => {
    console.log("Cliente WebSocket conectado");
    clientes.add(ws);

    if (ultimoSnapshot) {
        ws.send(JSON.stringify(ultimoSnapshot));
    } else {
        criarSnapshot(null, "ws-init")
            .then((snapshot) => {
                ultimoSnapshot = snapshot;
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify(snapshot));
                }
            })
            .catch((erro) => {
                console.error("Erro ao criar snapshot inicial:", erro);
            });
    }

    ws.on("close", () => clientes.delete(ws));
});

function notificarClientes(dados) {
    const msg = JSON.stringify(dados);
    clientes.forEach((ws) => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(msg);
        }
    });
}

function publicarSnapshot(snapshot) {
    ultimoSnapshot = snapshot;
    notificarClientes(snapshot);
}

async function criarSnapshot(status = null, origem = "soap") {
    const locacoes = await buscarLocacoes();
    const relatorio = gerarRelatorio(locacoes, status);

    return {
        evento: "relatorio_atualizado",
        origem,
        status,
        relatorio,
        atualizadoEm: new Date().toISOString(),
    };
}

// ── Lógica do relatório ───────────────────────────────
async function buscarLocacoes() {
    try {
        const response = await fetch("http://localhost:8002/api/locacoes");
        if (!response.ok) {
            return [];
        }

        return await response.json();
    } catch (erro) {
        console.error("Erro ao buscar locações:", erro.message);
        return [];
    }
}

function gerarRelatorio(locacoes, filtroStatus) {
    const filtradas = filtroStatus
        ? locacoes.filter(l => l.status === filtroStatus)
        : locacoes;

    return {
        total:      filtradas.length,
        reservados: filtradas.filter(l => l.status === "RESERVADO").length,
        em_uso:     filtradas.filter(l => l.status === "EM_USO").length,
        devolvidos: filtradas.filter(l => l.status === "DEVOLVIDO").length,
        atrasados:  filtradas.filter(l => l.status === "DEVOLVIDO_ATRASADO").length,
        cancelados: filtradas.filter(l => l.status === "CANCELADO").length,
    };
}

async function consultarRelatorio(status = null, origem = "soap") {
    const snapshot = await criarSnapshot(status, origem);

    publicarSnapshot(snapshot);

    return snapshot.relatorio;
}

app.get("/api/relatorio", async (req, res) => {
    try {
        const relatorio = await consultarRelatorio(req.query.status || null, "http");
        res.json({
            relatorio,
            atualizadoEm: ultimoSnapshot ? ultimoSnapshot.atualizadoEm : new Date().toISOString(),
        });
    } catch (erro) {
        console.error("Erro ao consultar relatório via HTTP:", erro);
        res.status(500).json({ erro: "Não foi possível consultar o relatório." });
    }
});

app.post("/api/relatorio/atualizar", async (req, res) => {
    try {
        const snapshot = await criarSnapshot(null, req.body?.origem || "event");
        publicarSnapshot(snapshot);

        res.json({
            relatorio: snapshot.relatorio,
            atualizadoEm: snapshot.atualizadoEm,
        });
    } catch (erro) {
        console.error("Erro ao atualizar relatório via webhook:", erro);
        res.status(500).json({ erro: "Não foi possível atualizar o relatório." });
    }
});

// ── Serviço SOAP ──────────────────────────────────────
const servico = {
    RelatorioService: {
        RelatorioPort: {
            consultarRelatorio: async (args) => {
                return consultarRelatorio(args?.status || null, "soap");
            }
        }
    }
};

// ── Subir servidor ────────────────────────────────────
const wsdl = fs.readFileSync(path.join(__dirname, "relatorios.wsdl"), "utf8");

soap.listen(server, "/relatorio", servico, wsdl, () => {
    console.log("SOAP rodando em http://localhost:9000/relatorio?wsdl");
});

server.listen(9000, () => {
    console.log("Servidor na porta 9000");
    console.log("WebSocket em ws://localhost:9000");
});