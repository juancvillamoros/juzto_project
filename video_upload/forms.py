from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    """Form for handling the Video model."""
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    class Meta:
        model = Video
        fields = ['cedula', 'id_audiencia', 'id_comparendo', 'video']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'id_audiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_comparendo': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        video = super().save(commit=False)
        video.user = self._user
        if commit:
            video.save()
        return video
