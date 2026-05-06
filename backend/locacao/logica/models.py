from django.db import models

from api_locacao_automoveis.backend.veiculos.logica.models import Veiculo

# Create your models here.
class Locacao(models.Model):
    class Status(models.TextChoices):
        RESERVADO = "RESERVADO", "Reservado"
        EM_USO = "EM_USO", "Em uso"
        DEVOLVIDO = "DEVOLVIDO", "Devolvido"
        DEVOLVIDO_ATRASADO = "DEVOLVIDO_ATRASADO", "Devolvido Atrasado"
        CANCELADO = "CANCELADO", "Cancelado"

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    cliente = models.CharField(max_length=100)
    dia_inicial = models.DateField(blank=False, null=False)
    dia_final = models.DateField(blank=False, null=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVADO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Locação #{self.id} - {self.cliente} - {self.veiculo.nome} ({self.status})"