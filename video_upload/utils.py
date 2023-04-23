import boto3
from typing import BinaryIO
from django.conf import settings
from .models import Video
import os
from typing import BinaryIO
import uuid
import moviepy.editor as mp


class VideoCompressor:
    def __init__(self, video_file: BinaryIO):
        self.video_file = video_file

    def compress_video(self) -> str:
        video_name = self.video_file.name
        video_temp_path = os.path.join(settings.BASE_DIR, 'video_temp')
        os.makedirs(video_temp_path, exist_ok=True)
        video_temp_file = os.path.join(video_temp_path, video_name)
        compressed_video_file = os.path.join(
            video_temp_path, f"{uuid.uuid4()}.mp4")
        video_clip = mp.VideoFileClip(video_temp_file)
        video_clip.write_videofile(compressed_video_file)
        video_clip.close()
        os.remove(video_temp_file)

        return compressed_video_file


# Conexión a AWS S3
class AwsS3Uploader:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_to_s3(self, video_file_path: str, video_s3_key: str) -> str:
        self.s3.upload_file(video_file_path, self.bucket_name, video_s3_key)
        os.remove(video_file_path)
        video_url = f"https://{self.bucket_name}.s3.amazonaws.com/{video_s3_key}"
        print(f"Video uploaded to {video_url}")
        return video_url


class VideoUploader:
    def __init__(self, cedula: str, id_audiencia: str, comparendo: str, video_url: str):
        self.cedula = cedula
        self.id_audiencia = id_audiencia
        self.comparendo = comparendo
        self.video_url = video_url

    def save_video_to_database(self):
        video_data = {
            "cedula": self.cedula,
            "id_audiencia": self.id_audiencia,
            "comparendo": self.comparendo,
            "video_url": self.video_url,
        }
        video = Video(**video_data)
        video.save()

        return self.video_url


def compress_and_upload_video(video_file: BinaryIO, cedula: str, id_audiencia: str, comparendo: str) -> str:
    # Comprimir el video y guardarlo en una carpeta temporal
    video_compressor = VideoCompressor(video_file)
    compressed_video_file = video_compressor.compress_video()

    # Subir el video comprimido a AWS S3
    s3_uploader = AwsS3Uploader()
    video_s3_key = f"{cedula}_{id_audiencia}_{comparendo}.mp4"
    video_url = s3_uploader.upload_to_s3(compressed_video_file, video_s3_key)

    # Guardar los datos en la base de datos
    video_uploader = VideoUploader(cedula, id_audiencia, comparendo, video_url)
    video_uploader.save_video_to_database()

    return video_url


class ZohoApiClient:
    def __init__(self):
        try:
            self.api_uri = settings.ZOHO_API_URL
            self.auth_token = settings.ZOHO_AUTH_TOKEN
        except AttributeError:
            raise ValueError(
                "ZOHO_API_URL and ZOHO_AUTH_TOKEN must be defined in settings.")


class ZohoIntegration:
    def __init__(self, id_audiencia: str, video_url: str, zoho_api_client: ZohoApiClient):
        self.id_audiencia = id_audiencia
        self.video_url = video_url
        self.zoho_api_client = zoho_api_client

    def update_video_url_in_zoho(self) -> bool:
        if not isinstance(self.id_audiencia, str) or not isinstance(self.video_url, str):
            raise TypeError("id_audiencia and video_url must be strings")
        if not self.id_audiencia.isalnum():
            raise ValueError("id_audiencia must be alphanumeric")

        video = Video.objects.filter(id_audiencia=self.id_audiencia).first()
        if not video:
            return False

        video.video_url = self.video_url
        video.save()

        self.zoho_api_client.update_video_url(
            self.id_audiencia, self.video_url)

        return True

    def integrate_video_url_with_zoho(self):
        try:
            zoho_record = self.zoho_api_client.get_zoho_record(
                self.id_audiencia)
            zoho_record["Video_URL"] = self.video_url
            self.zoho_api_client.update_zoho_record(
                self.id_audiencia, zoho_record)
            return True
        except Exception as e:
            print(f"Error integrating video URL with Zoho CRM: {e}")
            return False
