# movimientoInventario/views.py
from rest_framework import viewsets
from .serializers import MovimientoInventarioSerializer
from .models import MovimientoInventario

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    
    # def perform_create(self, serializer):
    #     # Aquí puedes agregar lógica adicional si lo necesitas, como registro de auditoría
    #     movimiento = serializer.save()

    #     # Si el tipo de movimiento es un ajuste manual, actualizamos el stock
    #     if movimiento.tipo_movimiento == 'ajuste':
    #         producto = movimiento.producto
    #         if movimiento.cantidad > 0:
    #             producto.stock += movimiento.cantidad
    #         elif movimiento.cantidad < 0:
    #             if producto.stock + movimiento.cantidad < 0:
    #                 raise serializers.ValidationError("No hay suficiente stock para realizar este ajuste.")
    #             producto.stock += movimiento.cantidad  # Decremento de stock

    #         producto.save()

    #     return movimiento

