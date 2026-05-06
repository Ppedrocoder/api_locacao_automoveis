def get_links_veiculo(veiculo_id: int, status: str) -> list:
    base = f"/api/veiculos/{veiculo_id}"

    links = [
        {"rel": "self", "href": base, "method": "GET"}
    ]

    if status == "Disponível":
        links.append({"rel": "reservar", "href": "/api/locacoes",              "method": "POST"  })
        links.append({"rel": "editar",   "href": base,                         "method": "PUT"   })
        links.append({"rel": "deletar",  "href": base,                         "method": "DELETE"})

    elif status == "Alugado":
        links.append({"rel": "locacao",  "href": f"/api/locacoes?veiculo_id={veiculo_id}", "method": "GET"})

    elif status == "Manutenção":
        links.append({"rel": "liberar",  "href": base, "method": "PATCH"})

    return links