from .models import Usuario, Pregunta, Respuesta
from .serializers import UsuarioSerializer, PreguntaSerializer, RespuestaSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import smtplib

from django.http import JsonResponse

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

def get_respuestas_usuarios():
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
    return rows

@api_view(["POST"])
def usuario_enviar_email(request):
    serializer = UsuarioSerializer(data = request.data)
    respuestas_usuarios = get_respuestas_usuarios()
    respuestas_body = ""
    for respuesta in respuestas_usuarios:
        respuestas_body = respuestas_body + respuesta + " <br/> "
    print(respuestas_body)
    if serializer.is_valid():
        correo = serializer.data.get('email')
        print('correo: ' , correo)
        username = "example@gmail.com"
        password = "123443"
        email_from = "example@gmail.com"
        email_to = [correo]
        subject = "Respuestas Usuarios"
        email_text = """\
                From: %s
                To: %s
                Subject: %s
                %s
                """ % (email_from, ", ".join(email_to), subject, respuestas_body)
    
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(username, password)
        server.sendmail(email_from, email_to, email_text)
        server.close()
        return Response({"detail": "EMAIL SENT"},content_type="application/json", status=status.HTTP_200_OK)
    else:
        return Response({"detail": "EMAIL NOT SENT"},content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

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
    respuestas_usuarios = get_respuestas_usuarios()
    return JsonResponse(respuestas_usuarios, safe=False)
