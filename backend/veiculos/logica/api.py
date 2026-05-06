from ninja import NinjaAPI
from .schemas import VeiculoSchema
from .models import Veiculo
from .hateoas import get_links_veiculo

api = NinjaAPI()

@api.get("/veiculos")
def listar_veiculos(request):
    veiculos = Veiculo.objects.all()
    return [
        {
            "id":          veiculo.id,
            "modelo":      veiculo.modelo,
            "marca":       veiculo.marca,
            "status":      veiculo.status,
            "tipo":        veiculo.tipo,
            "_links":      get_links_veiculo(veiculo.id, veiculo.status)
        }
        for veiculo in veiculos
    ]

@api.post("/veiculos")
def criar_veiculo(request, veiculo: VeiculoSchema):
    novo_veiculo = Veiculo.objects.create(modelo=veiculo.modelo, marca=veiculo.marca, status=veiculo.status, tipo=veiculo.tipo)
    return novo_veiculo

@api.get("/veiculos/{veiculo_id}")
def obter_veiculo(request, veiculo_id: int):
    veiculo = Veiculo.objects.get(id=veiculo_id)
    return {
        "id":          veiculo.id,
        "modelo":      veiculo.modelo,
        "marca":       veiculo.marca,
        "status":      veiculo.status,
        "tipo":        veiculo.tipo,
        "_links":      get_links_veiculo(veiculo.id, veiculo.status)
    }

@api.put("/veiculos/{veiculo_id}")
def atualizar_veiculo(request, veiculo_id: int, veiculo: VeiculoSchema):
    veiculo_atualizado = Veiculo.objects.filter(id=veiculo_id)
    veiculo_atualizado.update(modelo=veiculo.modelo, marca=veiculo.marca, status=veiculo.status, tipo=veiculo.tipo)
    return Veiculo.objects.get(id=veiculo_id)

@api.delete("/veiculos/{veiculo_id}")
def deletar_veiculo(request, veiculo_id: int):
    Veiculo.objects.filter(id=veiculo_id).delete()
    return {"message": "Veículo deletado com sucesso"}

@api.patch("/veiculos/{veiculo_id}/status")
def atualizar_status_veiculo(request, veiculo_id: int, status: str):
    veiculo = Veiculo.objects.get(id=veiculo_id)
    veiculo.status = status
    veiculo.save()
    return {"message": f"Status do veículo atualizado para {status} com sucesso"}
