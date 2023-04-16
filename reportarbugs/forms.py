from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csrfmiddlewaretoken'] = forms.CharField(widget=forms.HiddenInput())
