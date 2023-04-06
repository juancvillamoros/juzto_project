from django import forms

class VideoForm(forms.Form):
    cedula = forms.CharField(max_length=20)
    id_audiencia = forms.CharField(max_length=20)
    id_comparendo = forms.CharField(max_length=20)
    video = forms.FileField()
