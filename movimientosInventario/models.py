from django.db import models

from productos.models import Almacen, Producto


class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = (
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('ajuste', 'Ajuste Manual'),
    )
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_origen")
    almacen_destino = models.ForeignKey(Almacen, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimientos_destino")
    tipo_movimiento = models.CharField(max_length=10, choices=TIPOS_MOVIMIENTO)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} de {self.producto.nombre} ({self.cantidad} unidades)"    