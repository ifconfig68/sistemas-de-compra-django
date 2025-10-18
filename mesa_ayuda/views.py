from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Servicio , Usuario , Pedido  , Factura


def logout(request):
    try :
        del request.session["pista"]
        messages.success(request , "Sesion Cerrada con exito")
        return redirect("inicio")
    except KeyError:
         messages.error(request ,"Sesion no existe")
         return redirect ('inicio')
    except Exception as e :
        messages.error(request , f" Error cierre sesion {e}")
        return redirect('inicio')



def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")

        try :
            usuario = Usuario.objects.get(correo=correo  , contraseña= contraseña)
            messages.success(request, "Bienvenido!!")
            request.session["pista"] = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "nombre_rol": usuario.get_rol_display(),
            }
            return redirect('inicio')
        except Usuario.DoesNotExist :
            
             request.session["pista"] = None
             messages.warning(request, "Usuario o contraseña incorrectos...")
             return redirect('login')
        except Exception as e:
            request.session["pista"] = None
            messages.error(request, f"Ocurrió un error: {e}")
            return redirect('login')
    else :
        return render(request , "usuarios/login.html")


def registrarse (request ) : 
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")
        contraseña2 = request.POST.get("contraseña2")
        rol = request.POST.get("rol")
        try :
            if contraseña == contraseña2 : 
                usuario = Usuario(
                    nombre = nombre,
                    correo = correo,
                    contraseña = contraseña ,
                    rol = rol
                )
                if Usuario.objects.filter(correo=correo).exists():
                    messages.warning(request, "El correo ya está registrado.")
                    return redirect('registrarse')
                usuario.save()
                messages.success(request , "Registro Exitoso")
                return redirect ('inicio')
            else :
                messages.warning(request , "No concuerdan las contraseñas")
                return redirect("registrarse")
        except Exception as e :
            messages.error(request , f"Error: {e}")    
            return redirect ('registrarse')    

    else : 
        return render (request , "usuarios/registrar_usuario.html")
    

def listar_usuarios (request ) : 

    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('inicio')
    if usuario_info.get('rol') != 'A':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('inicio')  # Redirige a una página de sin permisos    
    
    


    listar = Usuario.objects.all()    
    print(listar)
    return render (request , "usuarios/listar_usuarios.html"  , {'listar' : listar})    


def eliminar_usuarios (request , id_usuario) :
    try :
        
        usuario  = Usuario.objects.get(pk = id_usuario)
        if usuario.rol == 'A' :
            messages.error(request, "No puedes eliminar un usuario con rol administrador.")
            return redirect('usuarios') 
        


        tiene_pedidos = Pedido.objects.filter(usuario=usuario, procesado=True).exists()
        if tiene_pedidos:
            messages.error(request, "No puedes eliminar este usuario porque ya tiene facturas asociadas.")
            return redirect('usuarios')
        





        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente!")
    except Usuario.DoesNotExist :
        messages.error(request , "el Usuario no existe")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
    
    return redirect("servicios")



            



# Create your views here.

def index(request)  : 
    return render(request , "index.html")


def servicios (request )  :
     return render(request , "servicios/servicios.html" )

def listar_servicios (request ) :

    n =1 
    for i in range(1,5) :
        print (" "*(4-i)*2 ,end=" ")
        for j in range(i):
            print(n , end=" ")
            n +=1
        print (" ")
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')    

    print("ok")
    listar = Servicio.objects.filter(activo=False)
    #print (listar)
    return render(request , "./servicios/listar_servicios.html" ,  {'listar' : listar})


def eliminar_servicios(request  , id_servicio) :
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')
    if usuario_info.get('rol') != 'A':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('login')  # Redirige a una página de sin permisos  
    try :
        q  = Servicio.objects.get(pk = id_servicio)
        q.delete()
        messages.success(request, "Servicio eliminado correctamente!")
    except Servicio.DoesNotExist :
        messages.error(request , "el servicio no existe")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")    
    return redirect("servicios")


def agregar_servicios(request) :  

    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')
    if usuario_info.get('rol') != 'A':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('login')  # Redirige a una página de sin permisos    
     

    if request.method == "POST" : 
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        activo = 'activo' in request.POST       
        try :         
            servicio = Servicio (
                nombre = nombre,
                precio = precio,
                descripcion = descripcion,
                tipo = tipo ,
                activo = activo
                )        
            servicio.save()
            messages.success(request ,"Servicio Agregado correctamente")
            return redirect('servicios')
        except Exception as e : 
                messages.error(request , f" Error al agegrar servicio {e}")                
        return redirect('servicios')              
    else:
        return render (request , './servicios/agregar.html')
    
def editar_servicios(request , id_servicio ) :
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')
    if usuario_info.get('rol') != 'A':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('login')  # Redirige a una página de sin permisos    
    

    if request.method == 'POST' :
        try :
            servicio = Servicio.objects.get(pk = id_servicio)
            servicio.nombre = request.POST.get('nombre')
            servicio.precio = request.POST.get('precio')
            servicio.descripcion = request.POST.get('descripcion')
            servicio.tipo = request.POST.get('tipo')
            servicio.activo = 'activo' in request.POST

            servicio.save()
            messages.success(request,  'Servicio Actualizado ')
            return redirect ('servicios')
        except Servicio.DoesNotExist :
            messages.error(request , 'Servicio no existe ') 
            return redirect ('servicios')
               
               
        except Exception as e :
            messages.error(request , f'error: {e}')    
            return redirect ('servicios')
    else :
        servicio = Servicio.objects.get(pk = id_servicio)
        data = {'data' : servicio}
        return render(request , "./servicios/agregar.html" , data)    


def agregar_orden(request):
  
  if request.method == "POST":
        # Obtener los IDs de los servicios seleccionados del formulario
        ids_servicios = request.POST.getlist('servicios')
               
        if not ids_servicios:
           return HttpResponse ("Sin seleccion ")  

        servicios = Servicio.objects.filter(id__in=ids_servicios)        

        request.session["servicios_seleccionados"] = ids_servicios
        orden_confirmada = request.session.pop("orden_confirmada", False)  

    

        

  return render (request ,"servicios/listar_servicios.html" , {'servicios' : servicios , 'orden_confirmada': orden_confirmada})


def confirmar_orden (request) :
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login') 

    servicios_guardados = request.session.get("servicios_seleccionados")
    usuario_dic = request.session.get("pista")
    

    if not usuario_dic:
        return HttpResponse("Sesión de usuario no disponible", status=403)

    if not servicios_guardados:
        return HttpResponse("No hay servicios seleccionados", status=400)

    try:
        usuario = Usuario.objects.get(id=usuario_dic["id"])
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)

    # Crear orden
    orden = Pedido.objects.create(usuario=usuario, procesado=False)

    # Asociar servicios
    servicios = Servicio.objects.filter(id__in=servicios_guardados)
    orden.servicios.add(*servicios)
    messages.success(request , "Orden creada con exito")

    # Limpiar la sesión
    del request.session["servicios_seleccionados"]
    
    return redirect('inicio')



def facturar (request) :
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')
        
    if usuario_info.get('rol') != 'A':
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('inicio')  # Redirige a una página de sin permisos      

    
    pedidos = Pedido.objects.filter(procesado=False).prefetch_related('servicios', 'usuario').order_by('-fecha_creacion')
    return render(request, 'servicios/facturar.html', {'pedidos': pedidos})
     
    

def historial_pedidos(request):
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')

    usuario_dic = request.session.get("pista")
    usuario_id = usuario_dic["id"]

    # Traer pedidos confirmados del usuario
    pedidos = Pedido.objects.filter(usuario_id=usuario_id).order_by('-fecha_creacion')

    return render(request, 'usuarios/historial_pedidos.html', {
        'pedidos': pedidos,
    })    


def procesar_pedidos(request):
    usuario_info = request.session.get('pista')
    if not usuario_info:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')
    
    if request.method == 'POST':
        ids_a_procesar = request.POST.getlist('pedidos')
        Pedido.objects.filter(id__in=ids_a_procesar).update(procesado=True)
        messages.success(request, f"pedido {ids_a_procesar } procesado ")
    return redirect('inicio')


def pagar_pedido (request , pedido_id ) : 
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect('mis_pedidos')

    try:
     pedido = Pedido.objects.get(id=pedido_id)
    except Pedido.DoesNotExist:
        messages.warning(request , "no se encuentra pedido")
       
       

    if pedido.pagado:
        messages.info(request, "Este pedido ya está pagado.")
    else:
        pedido.pagado = True
        pedido.save()
        messages.success(request, f"Pedido #{pedido.id} marcado como pagado.")
        return redirect('inicio')


    return redirect('mis_pedidos')
        

    
   


    

       
    

    
   

    
    



