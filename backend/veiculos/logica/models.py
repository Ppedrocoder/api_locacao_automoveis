from django.db import models

# Create your models here.
class Veiculo(models.Model):
    nome = models.CharField()
    tipo = models.CharField(choices='Carro, Moto'.strip(","))