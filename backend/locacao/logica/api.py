from .schemas import LocacaoSchema
from ninja import NinjaAPI
from .models import Locacao
from django.utils import timezone
from django.shortcuts import get_object_or_404
import httpx
from .hateoas import get_links
from .schemas import LocacaoOutSchema

api = NinjaAPI()

RELATORIOS_REFRESH_URL = "http://localhost:8000/api/relatorio/atualizar"


def notificar_relatorio(origem: str, status: str | None = None) -> None:
    try:
        httpx.post(
            RELATORIOS_REFRESH_URL,
            json={"origem": origem, "status": status},
            timeout=5.0,
        )
    except httpx.HTTPError as erro:
        print(f"[relatorio] Falha ao notificar atualização: {erro}")

@api.get("/locacoes", response=list[LocacaoOutSchema])
def listar_locacoes(request):
    locacoes = Locacao.objects.all()
    return [
        {
            "id":          locacao.id,
            "cliente":     locacao.cliente,
            "veiculo_id":  locacao.veiculo_id,
            "dia_inicial": locacao.dia_inicial,
            "dia_final":   locacao.dia_final,
            "status":      locacao.status,
            "links":      get_links(locacao.id, locacao.status)
        }
        for locacao in locacoes
    ]

@api.post("/locacoes")
def criar_locacao(request, locacao: LocacaoSchema):
    try:
        response = httpx.get(f"http://localhost:8001/api/veiculos/{locacao.veiculo_id}")
        if response.status_code == 404:
            return api.create_response(request, {"message": f"Veículo com ID {locacao.veiculo_id} não encontrado"}, status=404)
    except httpx.ConnectError:
        return api.create_response(request, {"message": "Serviço de veículos indisponível"}, status=503)

    nova_locacao = Locacao.objects.create(
        cliente=locacao.cliente,
        veiculo_id=locacao.veiculo_id,
        dia_inicial=locacao.dia_inicial,
        dia_final=locacao.dia_final
    )
    notificar_relatorio("locacao_criada")
    return {
        "id":         nova_locacao.id,
        "cliente":    nova_locacao.cliente,
        "veiculo_id": nova_locacao.veiculo_id,
        "dia_inicial": nova_locacao.dia_inicial,
        "dia_final":   nova_locacao.dia_final,
        "status":     nova_locacao.status,
        "links":      get_links(nova_locacao.id, nova_locacao.status)
    }

@api.get("/locacoes/{locacao_id}", response=LocacaoOutSchema)
def obter_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    return {
        "id":          locacao.id,
        "cliente":     locacao.cliente,
        "veiculo_id":  locacao.veiculo_id,
        "dia_inicial": locacao.dia_inicial,
        "dia_final":   locacao.dia_final,
        "status":      locacao.status,
        "links":      get_links(locacao.id, locacao.status)
    }

@api.delete("/locacoes/{locacao_id}")
def deletar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    if locacao.status not in ["DEVOLVIDO", "DEVOLVIDO_ATRASADO", "CANCELADO"]:
        return api.create_response(request, {"message": f"Locação não pode ser deletada pois está com status '{locacao.status}'"}, status=400)
    locacao.delete()
    notificar_relatorio("locacao_deletada")
    return {"message": "Locação deletada com sucesso"}

@api.put("/locacoes/{locacao_id}", response=LocacaoOutSchema)
def atualizar_locacao(request, locacao_id: int, locacao: LocacaoSchema):
    locacao_atualizada = get_object_or_404(Locacao, id=locacao_id)
    locacao_atualizada.cliente     = locacao.cliente
    locacao_atualizada.veiculo_id  = locacao.veiculo_id
    locacao_atualizada.dia_inicial = locacao.dia_inicial
    locacao_atualizada.dia_final   = locacao.dia_final
    locacao_atualizada.status      = locacao.status
    locacao_atualizada.save()
    notificar_relatorio("locacao_atualizada", locacao_atualizada.status)
    return get_object_or_404(Locacao, id=locacao_id)

@api.patch("/locacoes/{locacao_id}/finalizar")
def finalizar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    if locacao.status != "EM_USO":
        return api.create_response(request, {"message": f"Locação não pode ser finalizada pois está com status '{locacao.status}'"}, status=400)
    locacao.status = "DEVOLVIDO"
    if locacao.dia_final < timezone.now().date():
        locacao.status = "DEVOLVIDO_ATRASADO"
    locacao.save()
    notificar_relatorio("locacao_finalizada", locacao.status)
    return {"message": "Locação finalizada com sucesso"}

@api.patch("/locacoes/{locacao_id}/cancelar")
def cancelar_reserva(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    if locacao.status != "RESERVADO":
        return api.create_response(request, {"message": f"Locação não pode ser cancelada pois está com status '{locacao.status}'"}, status=400)
    locacao.status = "CANCELADO"
    locacao.save()
    notificar_relatorio("locacao_cancelada", locacao.status)
    return {"message": "Locação cancelada com sucesso"}

@api.patch("/locacoes/{locacao_id}/iniciar")
def iniciar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    if locacao.status != "RESERVADO":
        return api.create_response(request, {"message": f"Locação não pode ser iniciada pois está com status '{locacao.status}'"}, status=400)
    locacao.status = "EM_USO"
    locacao.save()
    notificar_relatorio("locacao_iniciada", locacao.status)
    return {"message": "Locação iniciada com sucesso"}