from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from juzto_project.settings import AWS_STORAGE_BUCKET_NAME
from .forms import VideoForm
from .models import Video
from .utils import compress_and_upload_to_s3

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener los datos del formulario
            cedula = form.cleaned_data['cedula']
            id_audiencia = form.cleaned_data['id_audiencia']
            id_comparendo = form.cleaned_data['id_comparendo']
            video_file = form.cleaned_data['video']
            
            # Crear instancia del modelo Video y guardar el archivo subido
            video = Video(cedula=cedula, id_audiencia=id_audiencia, id_comparendo=id_comparendo, video=video_file, user=request.user)
            video.save()
            
            try:
                # Llamar a la función para comprimir y subir el video a S3
                filename = f"{video.id}.mp4"
                content_type = "video/mp4"
                compress_and_upload_to_s3(video_file, filename, content_type)
                url = f"https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{filename}"
                
                # Guardar la URL en el modelo Video y guardar los cambios
                video.video_url = url
                video.save()
                
                # Enviar mensaje de éxito y redireccionar a la página principal
                messages.success(request, "¡El video ha sido cargado correctamente!")
                return redirect('dashboard')
            except Exception as e:
                # Manejar excepciones al subir el archivo a S3
                video.delete()
                messages.error(request, f"Error al subir el archivo: {str(e)}")
                return redirect('upload_video')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

@login_required
@permission_required('videos.view_video', raise_exception=True)
def video_list(request):
    user_id = request.user.id
    videos = Video.objects.filter(user_id=user_id).order_by('-fecha_subida')
    context = {'videos': videos}
    return render(request, 'video_list.html', context)
