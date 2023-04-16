from wsgiref.validate import validator
from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['cedula', 'id_audiencia', 'id_comparendo','video_url']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'id_audiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_comparendo': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_video_url(self):
        video_url = self.cleaned_data['video_url']
        if not validator.url(video_url):
            raise forms.ValidationError("Invalid URL")
        return video_url
