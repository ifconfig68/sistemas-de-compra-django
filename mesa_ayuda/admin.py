from django.contrib import admin
from .models import Servicio , Usuario , Factura , Pedido

# Register your models here.

@admin.register(Servicio) 
class ServicioAdmi(admin.ModelAdmin):
    list_display=['id' , 'nombre'  , 'precio' , 'tipo' , 'descripcion']


@admin.register(Usuario) 
class UsuarioAdmi(admin.ModelAdmin):
    list_display=['id' , 'nombre'  , 'correo' , 'fecha_creacion' , 'contraseña' , 'rol']




@admin.register(Factura) 
class FacturaAdmi(admin.ModelAdmin):
    list_display=['id' , 'usuario'  , 'total' , 'fecha_emision' , 'pagado']






@admin.register(Pedido) 
class PedidoAdmi(admin.ModelAdmin):
    list_display=['id' , 'usuario'  ,  'fecha_creacion' , 'procesado']

    

