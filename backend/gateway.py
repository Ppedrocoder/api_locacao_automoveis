# main.py

import asyncio
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from websockets import connect
from websockets.exceptions import ConnectionClosed

app = FastAPI(title="API Gateway")

# Adicionar CORS para aceitar requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "veiculos":   "http://localhost:8001",
    "locacoes":   "http://localhost:8002",
    "relatorios": "http://localhost:9000",
}

RELATORIOS_WS_URL = "ws://localhost:9000"

def chamar_servico(service: str, method: str, path: str, body=None, params=None):
    base_url = SERVICES.get(service)
    if not base_url:
        return {"error": f"Serviço '{service}' não encontrado"}

    url = f"{base_url}/api/{path}"

    try:
        print(f"[DEBUG] Chamando {method} {url}")
        response = httpx.request(
            method=method,
            url=url,
            json=body,
            params=params,
        )
        print(f"[DEBUG] Status: {response.status_code}")
        result = response.json()
        print(f"[DEBUG] Resposta: {result}")
        return result
    except httpx.ConnectError as e:
        error_msg = f"Serviço '{service}' indisponível"
        print(f"[ERROR] {error_msg}: {e}")
        return {"error": error_msg}


# ── Veículos ──────────────────────────────────────────
@app.get("/api/veiculos")
def listar_veiculos():
    return chamar_servico("veiculos", "GET", "veiculos")

@app.get("/api/veiculos/disponiveis")
def listar_veiculos_disponiveis():
    return chamar_servico("veiculos", "GET", "veiculos/disponiveis")

@app.get("/api/veiculos/{veiculo_id}")
def obter_veiculo(veiculo_id: int):
    return chamar_servico("veiculos", "GET", f"veiculos/{veiculo_id}")

@app.patch("/api/veiculos/{veiculo_id}/status")
def atualizar_status_veiculo(veiculo_id: int, status: str):
    return chamar_servico("veiculos", "PATCH", f"veiculos/{veiculo_id}/status", params={"status": status})


# ── Locações ──────────────────────────────────────────
@app.get("/api/locacoes")
def listar_locacoes():
    return chamar_servico("locacoes", "GET", "locacoes")

@app.get("/api/locacoes/{locacao_id}")
def obter_locacao(locacao_id: int):
    return chamar_servico("locacoes", "GET", f"locacoes/{locacao_id}")

@app.post("/api/locacoes")
def criar_locacao(payload: dict):
    return chamar_servico("locacoes", "POST", "locacoes", body=payload)

@app.patch("/api/locacoes/{locacao_id}/iniciar")
def iniciar_locacao(locacao_id: int):
    return chamar_servico("locacoes", "PATCH", f"locacoes/{locacao_id}/iniciar")

@app.patch("/api/locacoes/{locacao_id}/finalizar")
def finalizar_locacao(locacao_id: int):
    return chamar_servico("locacoes", "PATCH", f"locacoes/{locacao_id}/finalizar")

@app.patch("/api/locacoes/{locacao_id}/cancelar")
def cancelar_locacao(locacao_id: int):
    return chamar_servico("locacoes", "PATCH", f"locacoes/{locacao_id}/cancelar")

@app.delete("/api/locacoes/{locacao_id}")
def deletar_locacao(locacao_id: int):
    return chamar_servico("locacoes", "DELETE", f"locacoes/{locacao_id}")


# ── Relatórios ───────────────────────────────────────
@app.get("/api/relatorio")
def consultar_relatorio(status: str | None = None):
    params = {"status": status} if status else None
    return chamar_servico("relatorios", "GET", "relatorio", params=params)


@app.post("/api/relatorio/atualizar")
def atualizar_relatorio(payload: dict):
    return chamar_servico("relatorios", "POST", "relatorio/atualizar", body=payload)


@app.websocket("/ws/relatorio")
async def proxy_relatorio_ws(client_ws: WebSocket):
    await client_ws.accept()

    try:
        async with connect(RELATORIOS_WS_URL) as relatorio_ws:
            async def cliente_para_relatorio():
                while True:
                    mensagem = await client_ws.receive_text()
                    await relatorio_ws.send(mensagem)

            async def relatorio_para_cliente():
                while True:
                    mensagem = await relatorio_ws.recv()
                    if isinstance(mensagem, bytes):
                        await client_ws.send_bytes(mensagem)
                    else:
                        await client_ws.send_text(mensagem)

            await asyncio.gather(cliente_para_relatorio(), relatorio_para_cliente())

    except WebSocketDisconnect:
        pass
    except ConnectionClosed:
        pass
    except Exception as erro:
        print(f"[ERROR] Proxy websocket do relatório falhou: {erro}")

    try:
        await client_ws.close()
    except Exception:
        pass