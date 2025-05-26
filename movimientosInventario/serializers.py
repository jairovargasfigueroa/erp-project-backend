# inventario/serializers.py
from rest_framework import serializers
from .models import MovimientoInventario
from productos.models import Producto

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    almacen_origen_nombre = serializers.CharField(source='almacen_origen.nombre', read_only=True)
    almacen_destino_nombre = serializers.CharField(source='almacen_destino.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = MovimientoInventario
        fields = ['id', 'producto', 'cantidad', 'almacen_origen','almacen_origen_nombre','producto_nombre','almacen_destino_nombre', 'almacen_destino', 'tipo_movimiento', 'fecha_movimiento', 'referencia']
        read_only_fields = ['fecha_movimiento']
    
    def create(self, validated_data):
        # Creamos el movimiento de inventario
        movimiento = MovimientoInventario.objects.create(**validated_data)

        # Solo actualizamos el stock si es un ajuste manual
        if movimiento.tipo_movimiento == 'ajuste':
            producto = movimiento.producto
            if movimiento.cantidad > 0:
                # Si es un aumento, incrementamos el stock
                producto.stock += movimiento.cantidad
            elif movimiento.cantidad < 0:
                # Si es una disminución, decrementamos el stock
                if producto.stock + movimiento.cantidad < 0:
                    raise serializers.ValidationError("No hay suficiente stock para realizar este ajuste.")
                producto.stock += movimiento.cantidad  # Decrementamos el stock

            # Guardamos el producto con el stock actualizado
            producto.save()

        return movimiento


