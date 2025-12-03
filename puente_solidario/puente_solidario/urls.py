from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta línea agrega: login, logout, password_change, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Tus rutas de la aplicación
    path('', include('productos.urls')),
]