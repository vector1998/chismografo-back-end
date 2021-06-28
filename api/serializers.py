from rest_framework import serializers
from .models import Usuario, Pregunta, Respuesta

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'contrasena')

class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ('id', 'descripcion')

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ('id', 'usuario', 'pregunta', 'descripcion', 'fecha')