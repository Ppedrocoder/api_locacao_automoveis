# main.py

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
}

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