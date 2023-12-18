from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, CuotaHistorial

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'dni', 'apodo', 'fecha_inicio_cuota', 'fecha_fin_cuota']
        widgets = {
            'fecha_inicio_cuota': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_fin_cuota': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_inicio_cuota'].initial = self.instance.fecha_inicio_cuota
            self.fields['fecha_fin_cuota'].initial = self.instance.fecha_fin_cuota

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio_cuota")
        fecha_fin = cleaned_data.get("fecha_fin_cuota")

        # Verificar que la fecha de fin no sea anterior a la fecha de inicio solo si ambas están presentes
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

        # Aquí puedes añadir más validaciones si son necesarias
        # Por ejemplo, para evitar solapamientos con otras cuotas

        return cleaned_data

class CuotaHistorialForm(forms.ModelForm):
    class Meta:
        model = CuotaHistorial
        fields = ['fecha_inicio_cuota', 'fecha_fin_cuota']
        widgets = {
            'fecha_inicio_cuota': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_fin_cuota': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
        }
