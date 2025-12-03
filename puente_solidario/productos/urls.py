from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Secciones Públicas
    path('donar/', views.hacer_donacion, name='hacer_donacion'),
    path('trabajo/', views.trabajo, name='trabajo'),
    path('voluntariado/', views.voluntariado, name='voluntariado'),
    path('patrocinio/', views.patrocinio, name='patrocinio'),

    # Gestión Admin (Finanzas)
    path('finanzas/', views.lista_transacciones, name='lista_transacciones'),
    path('finanzas/nueva/', views.nueva_transaccion, name='nueva_transaccion'),
    path('finanzas/eliminar/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'),

    path('registro/', views.registro, name='registro'),
]