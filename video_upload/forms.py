from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['cedula', 'id_audiencia', 'id_comparendo','video']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'id_audiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_comparendo': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }