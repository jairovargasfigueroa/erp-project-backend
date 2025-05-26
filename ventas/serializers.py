from rest_framework import serializers

from movimientosInventario.models import MovimientoInventario
from .models import Venta, DetalleVenta
from clientes.models import Cliente
from productos.models import Producto

class DetalleVentaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre',read_only=True) 
    cliente_id = serializers.IntegerField(required=False)
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente_id', 'cliente_nombre','metodo_pago', 'promocion', 'fecha', 'total', 'detalles']
        read_only_fields = ['id', 'fecha', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        cliente_id = validated_data.pop('cliente_id', None)
        cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None

        total = 0
        venta = Venta.objects.create(cliente=cliente, **validated_data)

        for item in detalles_data:
            producto = Producto.objects.get(id=item['producto_id'])

            if producto.stock < item['cantidad']:
                raise serializers.ValidationError(
                    f"No hay stock suficiente para el producto '{producto.nombre}'. Disponible: {producto.stock}"
                )

            subtotal = producto.precio * item['cantidad']
            total += subtotal

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=producto.precio
            )

             # Registrar el movimiento de inventario
            MovimientoInventario.objects.create(
                producto=producto,
                cantidad=item['cantidad'],
                almacen_origen=producto.almacen,  # El almacén de origen será el almacén del producto
                almacen_destino=None,  # No hay almacén de destino para la venta
                tipo_movimiento="venta",  # Tipo de movimiento es venta
                referencia=f"Venta #{venta.id}"  # Información sobre la venta
            )
            
            producto.stock -= item['cantidad']
            producto.save()

        venta.total = total
        venta.save()

        return venta

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if instance.cliente:
            rep['cliente'] = {
                'id': instance.cliente.id,
                'nombre': instance.cliente.nombre
            }

        rep['detalles'] = [
            {
                'producto': {
                    'id': d.producto.id,
                    'nombre': d.producto.nombre
                },
                'cantidad': d.cantidad,
                'precio_unitario': (d.precio_unitario)
            }
            for d in instance.detalles.all()
        ]

        return rep
