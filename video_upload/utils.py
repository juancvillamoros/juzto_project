import os
import tempfile
from io import BytesIO
import boto3
from django.conf import settings
from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
from .models import Video


def compress_and_upload_to_s3(video_file, filename, content_type):
    """
    Comprime el video en formato mp4 y lo sube al bucket de S3 especificado en la configuración.
    Retorna la URL del archivo subido a S3.
    """
    # Verificar que el tamaño del video no supere los 3GB
    if video_file.size > 3 * 1024 * 1024 * 1024:
        raise ValueError("El tamaño del video no puede ser mayor a 3GB")

    # Crear carpeta temporal para almacenar el video
    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = os.path.join(temp_dir, "video.mp4")
        with open(video_path, 'wb+') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)

            # Abrir el archivo de video con moviepy y comprimirlo
            video = VideoFileClip(video_path)
            compressed_video = video.subclip().resize(height=720)
            compressed_video_bytes = BytesIO()
            compressed_video.write_videofile(compressed_video_bytes, codec='libx264', audio_codec='aac', fps=30)

            # Crear un cliente de S3 de AWS
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            # Subir el archivo comprimido a S3
            compressed_video_bytes.seek(0)
            s3.upload_fileobj(compressed_video_bytes, settings.AWS_STORAGE_BUCKET_NAME, filename, ExtraArgs={'ContentType': content_type})

            # Obtener la URL pública del archivo subido
            url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{filename}"

            # Borrar el video temporal
            os.remove(video_path)

            return url


def update_video_url_in_zoho(id_audiencia, video_url):
    try:
        # Actualizar el campo 'video' en el modelo Video
        video = Video.objects.get(id_audiencia=id_audiencia)
        video.video_url = video_url
        video.save()

        # Construir el cuerpo de la solicitud
        data = {
            "data": [
                {
                    "video": video_url
                }
            ]
        }

        # Enviar la solicitud a la API de Zoho
        url = f'http://ec2-44-207-20-96.compute-1.amazonaws.com/hearings/{id_audiencia}/'
        headers = {'Authorization': f'Bearer {settings.ZOHO_AUTH_TOKEN}'}
        response = requests.put(url, json=data, headers=headers)

        # Verificar que la solicitud se haya completado correctamente
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        # Manejar cualquier error que se produzca
        print(f'Error actualizando el campo "video" del modelo Video: {e}')
        return False
