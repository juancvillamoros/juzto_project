from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Reporte


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }



