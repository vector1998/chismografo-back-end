from rest_framework import generics
from .models import Usuario, Pregunta, Respuesta
from .serializers import UsuarioSerializer, PreguntaSerializer, RespuestaSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.http import JsonResponse

from api import serializers

#operaciones para usuarios
@api_view(["POST"])
def usuario_crear(request):
     serializer = UsuarioSerializer(data=request.data)
     if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def usuario_obtener(request , username, contrasena):
    usuario_existe = Usuario.objects.filter(username = username , contrasena = contrasena).exists()
    if usuario_existe :
       usuario = Usuario.objects.get(username = username , contrasena = contrasena)
       serializer = UsuarioSerializer(usuario)
       return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"usuario": "null"},content_type="application/json", status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def usuario_eliminar(request , usuario_id):
    usuario = Usuario.objects.get(id = usuario_id)
    if usuario != None :
       usuario.delete()
       return Response({"detail": "DELETED ELEMENT"},content_type="application/json", status=status.HTTP_200_OK)
    return Response({"detail": "NOT FOUND ELEMENT"},content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def usuario_enviar_email(request , email):
    body = render_to_string("email_content.html",{
        "name" : "victor",
        "message" : "hola como estas",
        "email" : "victoralejandromartinezmedina@gmail.com"
    })
    email_message = EmailMessage(
        subject="Respuestas",
        body=body,
        from_email="victoralejandromartinezmedina@gmail.com",
        to=[email]
    )
    email_message.content_subtype = "html"
    email_message.send()
    return Response({"detail": "EMAIL SENT"},content_type="application/json", status=status.HTTP_200_OK)

#operaciones para preguntas

@api_view(["POST"])
def pregunta_crear(request):
    serializer = PreguntaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def pregunta_obtener_todos(request):
    preguntas = Pregunta.objects.all()
    serializer = PreguntaSerializer(preguntas , many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#operaciones para respuestas
@api_view(["POST"])
def respuesta_crear(request):
    serializer = RespuestaSerializer(data=request.data)
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def respuesta_obtener_por_usuario(request , usuario_id):
    usuario = Usuario.objects.get(id = usuario_id)
    respuestas = Respuesta.objects.filter(usuario = usuario)
    if respuestas != None :
       serializer = RespuestaSerializer(respuestas , many = True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "ERROR"},content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def respuesta_actualizar(request , respuesta_id):
    respuesta = Respuesta.objects.get(id = respuesta_id)
    serializer = RespuestaSerializer(instance=respuesta, data=request.data, partial=True)
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "ERROR"},content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
       
@api_view(["GET"])
def respuesta_todos_usuarios(request):
    usuarios = Usuario.objects.all()
    preguntas = Pregunta.objects.all()
    rows = []
    row = "username | "
    
    for preguntaT in preguntas:
        row = row + preguntaT.descripcion + " | "
    rows.append(row)

    row = ""
    for usuarioT in usuarios:
        row = row + usuarioT.username + " | "
        for preguntaT in preguntas:
            respuesta = Respuesta.objects.get(usuario = usuarioT , pregunta = preguntaT)
            if respuesta == None:
               row = row + " NA " + " | "
            else:
               row = row + respuesta.descripcion + " | "
        rows.append(row)
        row = ""

    return JsonResponse(rows, safe=False)
