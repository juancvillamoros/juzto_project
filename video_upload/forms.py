from django import forms
from .models import Video
from .utils import VideoCompressor


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['cedula', 'id_audiencia', 'id_comparendo', 'video']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'id_audiencia': forms.TextInput(attrs={'class': 'form-control'}),
            'id_comparendo': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        if video:
            compressed_video_path = VideoCompressor(video)
            self.cleaned_data['video'] = compressed_video_path
        return cleaned_data
