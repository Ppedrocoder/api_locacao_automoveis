GATEWAY_URL = "http://localhost:8000"

def get_links(locacao_id: int, status: str) -> list:
    base = f"{GATEWAY_URL}/api/locacoes/{locacao_id}"

    links = [
        {"rel": "self", "href": base, "method": "GET"}
    ]

    if status == "RESERVADO":
        links.append({"rel": "iniciar",  "href": f"{base}/iniciar",  "method": "PATCH"})
        links.append({"rel": "cancelar", "href": f"{base}/cancelar", "method": "PATCH"})
        links.append({"rel": "editar",   "href": base,               "method": "PUT"  })

    elif status == "EM_USO":
        links.append({"rel": "finalizar", "href": f"{base}/finalizar", "method": "PATCH"})

    elif status in ("DEVOLVIDO", "DEVOLVIDO_ATRASADO"):
        links.append({"rel": "pagamento", "href": f"{GATEWAY_URL}/api/pagamentos/?locacao_id={locacao_id}", "method": "GET"})

    elif status == "CANCELADO":
        links.append({"rel": "deletar", "href": base, "method": "DELETE"})

    return links