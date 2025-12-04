from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Transaccion
from .forms import TransaccionForm, DonacionForm

def es_admin(user):
    return user.is_staff

def inicio(request):
    # Calcula totales y balance actual
    total_ingresos = Transaccion.objects.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = Transaccion.objects.filter(tipo='egreso').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = total_ingresos - total_egresos
    
    return render(request, 'productos/inicio.html', {
        'total_recaudado': total_ingresos,
        'total_distribuido': total_egresos,
        'total_disponible': balance
    })

def hacer_donacion(request):
    # Vista pública para donantes
    if request.method == 'POST':
        form = DonacionForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.tipo = 'ingreso'  # Fuerza el tipo a ingreso
            if not donacion.descripcion:
                donacion.descripcion = "Donación Anónima"
            donacion.save()
            return render(request, 'productos/donacion_exitosa.html')
    else:
        form = DonacionForm()
    return render(request, 'productos/donacion.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def nueva_transaccion(request):
    # Vista protegida: gestión administrativa completa
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:lista_transacciones')
    else:
        form = TransaccionForm()
    return render(request, 'productos/finanzas_form.html', {'form': form})

def lista_transacciones(request):
    transacciones = Transaccion.objects.all().order_by('-fecha')
    return render(request, 'productos/finanzas_lista.html', {'transacciones': transacciones})

def eliminar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('productos:lista_transacciones')
    return render(request, 'productos/eliminar_transaccion.html', {'transaccion': transaccion})

# Vistas estáticas informativas
def trabajo(request): return render(request, 'productos/trabajo.html')
def voluntariado(request): return render(request, 'productos/voluntariado.html')
def patrocinio(request): return render(request, 'productos/patrocinio.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Login automático tras registro
            return redirect('productos:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'productos/registro.html', {'form': form})