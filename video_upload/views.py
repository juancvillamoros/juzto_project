from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from .utils import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


@csrf_protect
@csrf_exempt
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el archivo de video del formulario
            video_file = request.FILES['video']

            # Comprimir el video
            compressor = VideoCompressor()
            compressed_video = compressor.compress(video_file)

            # Subir el video a S3
            s3_uploader = AwsS3Uploader()
            key_name = f"{form.cleaned_data['cedula']}/{form.cleaned_data['id_audiencia']}-{form.cleaned_data['id_comparendo']}.mp4"
            video_url = s3_uploader.upload(compressed_video, key_name)

            # Eliminar el archivo original
            video_uploader = VideoUploader(video_file)
            video_uploader.delete_files()

            # Actualizar la URL del video en Zoho
            zoho_api_client = ZohoApiClient(api_uri='https://api.zoho.com', auth_token='<YOUR_AUTH_TOKEN>')
            zoho_integration = ZohoIntegration(form.cleaned_data['id_audiencia'], video_url, zoho_api_client)
            zoho_integration.update_video_url()

            # Crear una instancia del modelo Video y guardarla en la base de datos
            video = form.save(commit=False)
            video.user = request.user
            video.video_url = video_url
            video.save()

            return redirect('video_list')
    else:
        form = VideoForm()

    return render(request, 'upload_video.html', {'form': form})


@login_required
def video_list(request):
    videos = Video.objects.filter(user=request.user)
    return render(request, 'video_list.html', {'videos': videos})
