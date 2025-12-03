from django import forms
from .models import Transaccion

# --- FORMULARIO PARA ADMIN (Gestión Completa) ---
class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detalle del movimiento'}),
        }
        labels = {
            'tipo': 'Tipo de Movimiento',
            'monto': 'Monto ($)',
            'descripcion': 'Descripción',
        }

# --- FORMULARIO PARA USUARIO (Solo Donar) ---
class DonacionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['monto', 'descripcion'] # El usuario NO ve el tipo (siempre es Ingreso)
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '¿Cuánto quieres aportar?'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre o mensaje de apoyo'}),
        }
        labels = {
            'monto': 'Monto del Aporte ($)',
            'descripcion': 'Mensaje (Opcional)',
        }