from django.db import models

# Create your models here.
class Veiculo(models.Model):
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('Disponível', 'Disponível'), ('Alugado', 'Alugado')], default='Disponível')
    tipo = models.CharField(max_length=20, choices=[('Carro', 'Carro'), ('Moto', 'Moto')])