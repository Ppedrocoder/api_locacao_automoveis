from ninja import NinjaAPI
from .schemas import VeiculoOutSchema, VeiculoSchema
from .models import Veiculo
from .hateoas import get_links_veiculo
from django.shortcuts import get_object_or_404

api = NinjaAPI()

@api.get("/veiculos", response=list[VeiculoOutSchema])
def listar_veiculos(request):
    veiculos = Veiculo.objects.all()
    return [
        {
            "id":     veiculo.id,
            "modelo": veiculo.modelo,
            "marca":  veiculo.marca,
            "status": veiculo.status,
            "tipo":   veiculo.tipo,
            "links":  get_links_veiculo(veiculo.id, veiculo.status)  # ← era "_links"
        }
        for veiculo in veiculos
    ]

@api.post("/veiculos", response=VeiculoOutSchema)
def criar_veiculo(request, veiculo: VeiculoSchema):
    novo = Veiculo.objects.create(
        modelo=veiculo.modelo,
        marca=veiculo.marca,
        tipo=veiculo.tipo
    )
    return {
        "id":     novo.id,
        "modelo": novo.modelo,
        "marca":  novo.marca,
        "status": novo.status,
        "tipo":   novo.tipo,
        "links":  get_links_veiculo(novo.id, novo.status)  # ← adiciona isso
    }

@api.get("/veiculos/{veiculo_id}", response=VeiculoOutSchema)
def obter_veiculo(request, veiculo_id: int):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)  # ← retorna 404 corretamente
    return {
        "id":     veiculo.id,
        "modelo": veiculo.modelo,
        "marca":  veiculo.marca,
        "status": veiculo.status,
        "tipo":   veiculo.tipo,
        "links":  get_links_veiculo(veiculo.id, veiculo.status)
    }

@api.put("/veiculos/{veiculo_id}", response=VeiculoOutSchema)
def atualizar_veiculo(request, veiculo_id: int, veiculo: VeiculoSchema):
    Veiculo.objects.filter(id=veiculo_id).update(
        modelo=veiculo.modelo,
        marca=veiculo.marca,
        status=veiculo.status,
        tipo=veiculo.tipo
    )
    v = Veiculo.objects.get(id=veiculo_id)
    return {
        "id":     v.id,
        "modelo": v.modelo,
        "marca":  v.marca,
        "status": v.status,
        "tipo":   v.tipo,
        "links":  get_links_veiculo(v.id, v.status)  # ← adiciona isso
    }

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
