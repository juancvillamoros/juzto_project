from django import forms
from .models import Video
from .utils import VideoCompressor


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['cedula', 'id_audiencia', 'id_comparendo', 'video_url']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'id_audiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_comparendo': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        if video_url:
            compressed_video_path = VideoCompressor(video_url)
            self.cleaned_data['video_url'] = compressed_video_path
        return cleaned_data
