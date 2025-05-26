import re
from rest_framework import serializers

from movimientosInventario.models import MovimientoInventario
from .models import Compra, DetalleCompra
from productos.models import Producto
from proveedores.models import Proveedor

class DetalleCompraSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()
    
class CompraSerializer(serializers.ModelSerializer):
    proveedor_id = serializers.IntegerField(required=False)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre',read_only=True)
    detalles = DetalleCompraSerializer(many=True)    
    
    class Meta:
        model = Compra
        fields = ['id', 'proveedor_id','proveedor_nombre', 'metodo_pago', 'promocion', 'fecha', 'total', 'detalles']
        read_only_fields = ['id', 'fecha', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        proveedor_id = validated_data.pop('proveedor_id', None)
        proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None

        total = 0
        compra = Compra.objects.create(proveedor=proveedor, **validated_data)

        for item in detalles_data:
            producto = Producto.objects.get(id=item['producto_id'])

            subtotal = producto.precio * item['cantidad']  # Usa precio_compra para compras
            total += subtotal

            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=producto.precio
            )
            
             # Registrar el movimiento de inventario
            MovimientoInventario.objects.create(
                producto=producto,
                cantidad=item['cantidad'],
                almacen_origen=None,  # No aplica para compras
                almacen_destino=producto.almacen,  # El almacén de destino será el almacén del producto
                tipo_movimiento="compra",  # Tipo de movimiento es compra
                referencia=f"Compra #{compra.id}"  # Información sobre la compra
            )


            producto.stock += item['cantidad']  # Incrementar stock al comprar
            producto.save()

        compra.total = total
        compra.save()

        return compra

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if instance.proveedor:
            rep['proveedor'] = {
                'id': instance.proveedor.id,
                'nombre': instance.proveedor.nombre
            }

        rep['detalles'] = [
            {
                'producto': {
                    'id': d.producto.id,
                    'nombre': d.producto.nombre
                },
                'cantidad': d.cantidad,
                'precio_unitario': float(d.precio_unitario)
            }
            for d in instance.detalles.all()
        ]

        return rep