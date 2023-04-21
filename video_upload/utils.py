import boto3
import subprocess

from io import BytesIO
from typing import BinaryIO
from .models import Video
from django.conf import settings


class VideoCompressor:
    def __init__(self, max_size: int = 3000000000, quality: str = 'hd', output_dir: str = 'temp'):
        self.max_size = max_size
        self.quality = quality
        self.output_dir = output_dir

    def compress(self, video_file: BinaryIO) -> BinaryIO:
        # Comando para comprimir el video
        command = [
            "ffmpeg",
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            "-f",
            "mp4",
            "-"
        ]

        # Ejecutar el comando
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        compressed_video_bytes = BytesIO(
            process.communicate(input=video_file.read())[0])

        # Verificar si hubo algún error en la compresión
        if process.returncode != 0:
            raise Exception("Error comprimiendo el video")

        # Verificar el tamaño del archivo comprimido
        if compressed_video_bytes.getbuffer().nbytes > self.max_size:
            raise Exception(
                "El tamaño del archivo comprimido es mayor al tamaño máximo permitido")

        return compressed_video_bytes


class S3Uploader:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload(self, compressed_video_bytes: BinaryIO, key_name: str) -> str:
        self.s3.upload_fileobj(compressed_video_bytes,
                               self.bucket_name, key_name)
        url = f"https://{self.bucket_name}.s3.amazonaws.com/{key_name}"
        return url


class VideoUploader:
    def __init__(self, video_file: BinaryIO):
        self.video_file = video_file

    def upload(self, compressed_video_bytes: BinaryIO, key_name: str) -> str:
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3.upload_fileobj(compressed_video_bytes, bucket_name, key_name)
        url = f"https://{bucket_name}.s3.amazonaws.com/{key_name}"
        return url

    def delete_files(self):
        self.video_file.close()


class ZohoApiClient:
    def __init__(self, api_uri: str, auth_token: str):
        self.api_uri = api_uri
        self.auth_token = auth_token

    def update_video_url(self, id_audiencia: str, video_url: str) -> bool:
        # Lógica para actualizar la URL del video en Zoho
        pass


class ZohoIntegration:
    def __init__(self, id_audiencia: str, video_url: str, zoho_api_client: ZohoApiClient):
        self.id_audiencia = id_audiencia
        self.video_url = video_url
        self.zoho_api_client = zoho_api_client

    def update_video_url_in_zoho(self) -> bool:
        if not isinstance(self.id_audiencia, str) or not isinstance(self.video_url, str):
            raise TypeError("id_audiencia and video_url must be strings")
        if not self.id_audiencia.isnumeric():
            raise ValueError("id_audiencia must be numeric")

        video = Video.objects.filter(id_audiencia=self.id_audiencia).first()
        if not video:
            return False

        video.video_url = self.video_url
        video.save()

        self.zoho_api_client.update_video_url(
            self.id_audiencia, self.video_url)

        return True
