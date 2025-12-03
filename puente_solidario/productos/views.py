from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaccion
from .forms import TransaccionForm, DonacionForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def es_admin(user):
    return user.is_staff

# ... (Tu vista de inicio se mantiene igual) ...
def inicio(request):
    total_ingresos = Transaccion.objects.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = Transaccion.objects.filter(tipo='egreso').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = total_ingresos - total_egresos
    return render(request, 'productos/inicio.html', {
        'total_recaudado': total_ingresos,
        'total_distribuido': total_egresos,
        'total_disponible': balance
    })

# --- VISTA 1: DONACIÓN PÚBLICA (Usa DonacionForm y donacion.html) ---
def hacer_donacion(request):
    if request.method == 'POST':
        form = DonacionForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.tipo = 'ingreso'  # <-- SIEMPRE es Ingreso
            if not donacion.descripcion:
                donacion.descripcion = "Donación Anónima"
            donacion.save()
            return render(request, 'productos/donacion_exitosa.html')
    else:
        form = DonacionForm()
    
    # Renderiza la plantilla bonita de donaciones
    return render(request, 'productos/donacion.html', {'form': form})


# --- VISTA 2: GESTIÓN ADMIN (Usa TransaccionForm y finanzas_form.html) ---
@login_required
@user_passes_test(es_admin)
def nueva_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save() # Guarda lo que el admin eligió (Ingreso o Gasto)
            return redirect('productos:lista_transacciones')
    else:
        form = TransaccionForm()
    
    # Renderiza la plantilla técnica de administración
    return render(request, 'productos/finanzas_form.html', {'form': form})

# ... (Mantén tus otras vistas: lista_transacciones, editar, eliminar, etc.) ...
def lista_transacciones(request):
    transacciones = Transaccion.objects.all().order_by('-fecha')
    return render(request, 'productos/finanzas_lista.html', {'transacciones': transacciones})

def eliminar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('productos:lista_transacciones')
    return render(request, 'productos/eliminar_transaccion.html', {'transaccion': transaccion})

# ... (Vistas estáticas: trabajo, voluntariado, patrocinio) ...
def trabajo(request): return render(request, 'productos/trabajo.html')
def voluntariado(request): return render(request, 'productos/voluntariado.html')
def patrocinio(request): return render(request, 'productos/patrocinio.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Loguear al usuario inmediatamente después de registrarse
            login(request, user)
            return redirect('productos:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'productos/registro.html', {'form': form})