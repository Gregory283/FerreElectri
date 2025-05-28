from django.db import models

# Create your models here.

class Ventas(models.Model):
    numero = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=25, unique=True)
    articulo = models.CharField(max_length=25)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.Nombre