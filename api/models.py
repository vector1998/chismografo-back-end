from django.db import models

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=20)
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=300)
    def __str__(self):
        return self.username

class Pregunta(models.Model):
    descripcion = models.TextField()
    def __str__(self):
        return self.descripcion

class Respuesta(models.Model):
    usuario = models.ForeignKey(Usuario , on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta , on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250)
    fecha = models.DateTimeField()
    def __str__(self):
        return self.descripcion
