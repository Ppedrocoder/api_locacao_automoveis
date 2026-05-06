# main.py

import httpx
from fastapi import FastAPI

app = FastAPI(title="API Gateway")

SERVICES = {
    "veiculos":   "http://localhost:8001",
    "locacoes":   "http://localhost:8002",
    "pagamentos": "http://localhost:8003",
}

def chamar_servico(service: str, method: str, path: str, body=None, params=None):
    base_url = SERVICES.get(service)
    if not base_url:
        return {"error": f"Serviço '{service}' não encontrado"}

    url = f"{base_url}/api/{path}"

    try:
        response = httpx.request(
            method=method,
            url=url,
            json=body,
            params=params,
        )
        return response.json()
    except httpx.ConnectError:
        return {"error": f"Serviço '{service}' indisponível"}


# ── Veículos ──────────────────────────────────────────
@app.get("/api/veiculos")
def listar_veiculos():
    return chamar_servico("veiculos", "GET", "veiculos")

@app.get("/api/veiculos/{veiculo_id}")
def obter_veiculo(veiculo_id: int):
    return chamar_servico("veiculos", "GET", f"veiculos/{veiculo_id}")


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