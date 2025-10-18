from django.db import models
from django.utils import timezone

# Create your models here.
class Servicio (models.Model) :
    TIPOS = (
       ("P" , "PUBLICITARIO"),
       ("T" , "TECNOLOGICO"),
       
    )

    nombre = models.CharField(max_length=100)
    precio = models.CharField(max_length=200 , default="")
    descripcion = models.TextField (default="Disponible")
    tipo = models.CharField(max_length=1 , choices=TIPOS , default= 'T')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)


    def  __str__ (self) :
        return self.nombre
    

class Usuario(models.Model):
    ROLES = (
        ("A", "Administrador"),
        ("U", "Usuario"),       
    )
    nombre = models.CharField(max_length=100) 
    correo = models.EmailField(unique=True)   
    contraseña =  models.CharField(max_length=100 , default= "") 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=1, choices=ROLES, default="U")

    def __str__(self):
        return f"{self.nombre}"
    
class Factura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)

    def calcular_total(self):
        total = sum(servicio.precio for servicio in self.servicios.all())
        self.total = total
        self.save()

    def __str__(self):
        return f"Factura {self.id} - {self.usuario.nombre}"



class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido de {self.usuario.nombre}"
