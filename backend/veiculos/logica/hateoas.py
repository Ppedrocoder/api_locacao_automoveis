GATEWAY_URL = "http://localhost:8000"

def get_links_veiculo(veiculo_id: int, status: str) -> list:
    base = f"{GATEWAY_URL}/api/veiculos/{veiculo_id}"

    links = [
        {"rel": "self", "href": base, "method": "GET"}
    ]

    if status == "Disponível":
        links.append({"rel": "reservar", "href": f"{GATEWAY_URL}/api/locacoes",              "method": "POST"  })
        links.append({"rel": "editar",   "href": base,                                        "method": "PUT"   })
        links.append({"rel": "deletar",  "href": base,                                        "method": "DELETE"})

    elif status == "Alugado":
        links.append({"rel": "locacao",  "href": f"{GATEWAY_URL}/api/locacoes?veiculo_id={veiculo_id}", "method": "GET"})

    return links