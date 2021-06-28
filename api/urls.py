from django.urls import path
from api import views

urlpatterns = [
    path('usuario/', views.usuario_crear ),
    path('usuario/<slug:username>/<slug:contrasena>/', views.usuario_obtener),
    path('usuario/<int:usuario_id>/', views.usuario_eliminar),
    path('usuario/correo/', views.usuario_enviar_email),
    path('pregunta/', views.pregunta_crear),
    path('pregunta/todo/', views.pregunta_obtener_todos),
    path('respuesta/', views.respuesta_crear),
    path('respuesta/<int:usuario_id>/', views.respuesta_obtener_por_usuario),
    path('respuesta/actualizar/<int:respuesta_id>/', views.respuesta_actualizar),
    path('respuesta/usuarios/', views.respuesta_todos_usuarios)
]