# inventario/serializers.py
from rest_framework import serializers
from .models import MovimientoInventario
from productos.models import Producto

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    fecha_movimiento = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)  # Formato día/mes/año hora:minuto:segundo
    almacen_origen_nombre = serializers.CharField(source='almacen_origen.nombre', read_only=True)
    almacen_destino_nombre = serializers.CharField(source='almacen_destino.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = MovimientoInventario
        fields = ['id', 'producto', 'cantidad', 'almacen_origen','almacen_origen_nombre','producto_nombre','almacen_destino_nombre', 'almacen_destino', 'tipo_movimiento', 'fecha_movimiento', 'referencia']
        read_only_fields = ['fecha_movimiento']
    
    def create(self, validated_data):
        movimiento = MovimientoInventario.objects.create(**validated_data)

        producto = movimiento.producto
        cantidad = movimiento.cantidad
        origen = movimiento.almacen_origen
        destino = movimiento.almacen_destino

        # --- TRASLADO SIMULADO (ajuste con origen y destino distintos) ---
        if movimiento.tipo_movimiento == 'ajuste' and origen and destino and origen != destino:
            if producto.stock < cantidad:
                raise serializers.ValidationError("Stock insuficiente para traslado.")

            # 1. Restar del producto original (en origen)
            producto.stock -= cantidad
            producto.save()

            # 2. Buscar si ya existe el producto en el destino
            filtro = {
                'nombre': producto.nombre,
                'almacen': destino
            }
            if producto.categoria:
                filtro['categoria'] = producto.categoria

            producto_destino = Producto.objects.filter(**filtro).first()

            if producto_destino:
                producto_destino.stock += cantidad
                producto_destino.save()
            else:
                # Crear nuevo producto en almacén destino con mismo nombre
                Producto.objects.create(
                    nombre=producto.nombre,
                    descripcion=producto.descripcion,
                    precio=producto.precio,
                    imagen=producto.imagen,
                    stock=cantidad,
                    categoria=producto.categoria,
                    almacen=destino
                )

        # --- AJUSTE NORMAL ---
        else:
            if cantidad > 0:
                producto.stock += cantidad
            elif cantidad < 0:
                if producto.stock + cantidad < 0:
                    raise serializers.ValidationError("No hay suficiente stock para realizar este ajuste.")
                producto.stock += cantidad
            producto.save()

        return movimiento
    # def create(self, validated_data):
    #     movimiento = MovimientoInventario.objects.create(**validated_data)

    #     producto = movimiento.producto
    #     cantidad = movimiento.cantidad
    #     origen = movimiento.almacen_origen
    #     destino = movimiento.almacen_destino

    #     print(f"Tipo: {movimiento.tipo_movimiento} | Producto: {producto} | Cantidad: {cantidad}")
    #     print(f"Origen: {origen} | Destino: {destino}")

    #     if movimiento.tipo_movimiento == 'ajuste':
    #         print(">>> AJUSTE")
    #         if cantidad > 0:
    #             producto.stock += cantidad
    #         elif cantidad < 0:
    #             if producto.stock + cantidad < 0:
    #                 raise serializers.ValidationError("No hay suficiente stock para realizar este ajuste.")
    #             producto.stock += cantidad
    #         producto.save()
    #         print(f"Stock ajustado: {producto.stock}")

    #     elif origen and destino and origen != destino:
    #         print(">>> TRASLADO ENTRE ALMACENES")

    #         if producto.stock < cantidad:
    #             raise serializers.ValidationError("Stock insuficiente para traslado.")

    #         producto.stock -= cantidad
    #         producto.save()
    #         print(f"Stock restado en origen: {producto.stock}")

    #         filtro = {
    #             'nombre': producto.nombre,
    #             'almacen': destino
    #         }
    #         if producto.categoria:
    #             filtro['categoria'] = producto.categoria

    #         print(f"Buscando producto destino con filtro: {filtro}")
    #         producto_destino = Producto.objects.filter(**filtro).first()

    #         if producto_destino:
    #             print(">>> Producto destino ya existe. Sumando stock...")
    #             producto_destino.stock += cantidad
    #             producto_destino.save()
    #             print(f"Nuevo stock destino: {producto_destino.stock}")
    #         else:
    #             print(">>> Producto destino NO existe. Creando nuevo...")
    #             nuevo_producto = Producto.objects.create(
    #                 nombre=producto.nombre,
    #                 descripcion=producto.descripcion,
    #                 precio=producto.precio,
    #                 imagen=producto.imagen,
    #                 stock=cantidad,
    #                 categoria=producto.categoria,
    #                 almacen=destino
    #             )
    #             print(f"Producto creado en destino con ID: {nuevo_producto.id}")

    #     elif destino and not origen:
    #         print(">>> COMPRA - aumento de stock")
    #         producto.stock += cantidad
    #         producto.save()

    #     elif origen and not destino:
    #         print(">>> VENTA - disminución de stock")
    #         if producto.stock < cantidad:
    #             raise serializers.ValidationError("No hay suficiente stock para esta venta.")
    #         producto.stock -= cantidad
    #         producto.save()

    #     return movimiento



