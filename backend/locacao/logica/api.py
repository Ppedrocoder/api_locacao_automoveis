from api_locacao_automoveis.backend.locacao.logica.schemas import LocacaoSchema
from ninja import NinjaAPI
from .models import Locacao
from api_locacao_automoveis.backend.veiculos.logica.models import Veiculo
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .hateoas import get_links

api = NinjaAPI()

@api.get("/locacoes")
def listar_locacoes(request):
    locacoes = Locacao.objects.all()
    return [
        {
            "id":          locacao.id,
            "cliente":     locacao.cliente,
            "veiculo":     str(locacao.veiculo),
            "dia_inicial": locacao.dia_inicial,
            "dia_final":   locacao.dia_final,
            "status":      locacao.status,
            "_links":      get_links(locacao.id, locacao.status)
        }
        for locacao in locacoes
    ]

@api.post("/locacoes")
def criar_locacao(request, locacao: LocacaoSchema):
    veiculo = get_object_or_404(Veiculo, id=locacao.veiculo_id)
    if veiculo.status != "Disponível":
        return {"message": f"Veículo {veiculo.modelo} não está disponível"}
    Locacao.objects.create(
        cliente=locacao.cliente,
        veiculo=veiculo,
        dia_inicial=locacao.dia_inicial,
        dia_final=locacao.dia_final
    )
    veiculo.status = "Alugado"
    veiculo.save()
    return {"message": f"Veículo {veiculo.modelo} reservado com sucesso"}

@api.get("/locacoes/{locacao_id}")
def obter_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    return {
        "id":          locacao.id,
        "cliente":     locacao.cliente,
        "veiculo":     str(locacao.veiculo),
        "dia_inicial": locacao.dia_inicial,
        "dia_final":   locacao.dia_final,
        "status":      locacao.status,
        "_links":      get_links(locacao.id, locacao.status)
    }

@api.delete("/locacoes/{locacao_id}")
def deletar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    locacao.delete()
    return {"message": "Locação deletada com sucesso"}

@api.put("/locacoes/{locacao_id}")
def atualizar_locacao(request, locacao_id: int, locacao: LocacaoSchema):
    veiculo = get_object_or_404(Veiculo, id=locacao.veiculo_id)
    locacao_atualizada = get_object_or_404(Locacao, id=locacao_id)
    locacao_atualizada.cliente = locacao.cliente
    locacao_atualizada.veiculo = veiculo
    locacao_atualizada.dia_inicial = locacao.dia_inicial
    locacao_atualizada.dia_final = locacao.dia_final
    locacao_atualizada.status = locacao.status
    locacao_atualizada.save()
    return Locacao.objects.get(id=locacao_id)

@api.patch("/locacoes/{locacao_id}/finalizar")
def finalizar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    veiculo = locacao.veiculo
    if veiculo.status == "Alugado":
        veiculo.status = "Disponível"
        veiculo.save()
        locacao.status = "DEVOLVIDO"
        if locacao.dia_final < timezone.now().date():
            locacao.status = "DEVOLVIDO_ATRASADO"
        locacao.save()
        return {"message": f"Locação do veículo {veiculo.modelo} finalizada com sucesso"}
    else:
        return {"message": f"Veículo {veiculo.modelo} não está em uso para finalizar locação"}

    
@api.patch("/locacoes/{locacao_id}/cancelar")
def cancelar_reserva(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    veiculo = locacao.veiculo
    if veiculo.status == "Alugado":
        veiculo.status = "Disponível"
        veiculo.save()
        locacao.status = "CANCELADO"
        locacao.save()
        return {"message": f"Reserva do veículo {veiculo.modelo} cancelada com sucesso"}
    else:
        return {"message": f"Veículo {veiculo.modelo} não está reservado para cancelar reserva"}

@api.patch("/locacoes/{locacao_id}/iniciar")
def iniciar_locacao(request, locacao_id: int):
    locacao = get_object_or_404(Locacao, id=locacao_id)
    veiculo = locacao.veiculo
    if veiculo.status == "Alugado":
        locacao.status = "EM_USO"
        locacao.save()
        return {"message": f"Veículo {veiculo.modelo} iniciado para locação com sucesso"}
    else:
        return {"message": f"Veículo {veiculo.modelo} já está em uso ou não está reservado para iniciar locação"}