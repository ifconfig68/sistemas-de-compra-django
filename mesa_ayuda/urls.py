from django.urls import path
from . import views   

urlpatterns = [
    path('' , views.index , name = 'inicio'),
    path('servicios/',views.servicios , name='servicios'),   
    path("eliminar_servicios/<int:id_servicio>/", views.eliminar_servicios, name="eliminar_servicios"),
    path("agregar_servicios/", views.agregar_servicios, name="agregar_servicios"),
    path("editar_servicios/<int:id_servicio>/", views.editar_servicios, name="editar_servicios"),
    path("listar_servicios/", views.listar_servicios, name="listar_servicios"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registrarse/", views.registrarse, name="registrarse"),
    path("usuarios/", views.listar_usuarios, name="usuarios"),
    path("eliminar_usuarios/<int:id_usuario>/", views.eliminar_usuarios, name="eliminar_usuarios"),
    path("agregar_orden/", views.agregar_orden, name="agregar_orden"),
    path("confirmar_orden/", views.confirmar_orden, name="confirmar_orden"),
    path("facturar/", views.facturar, name="facturar"),
    path("mis_pedidos/", views.historial_pedidos, name="mis_pedidos"),
    path("procesar_pedidos/", views.procesar_pedidos, name="procesar_pedidos"),
    path("pedido/<int:pedido_id>/pagar/", views.pagar_pedido, name="pagar_pedido"),
    



    

]
