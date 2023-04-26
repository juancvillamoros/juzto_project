import os
import uuid
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

s3 = S3Boto3Storage()

def get_unique_file_name(file_path):
    """Returns a unique file name by adding a suffix to the file name if it already exists."""
    if not os.path.exists(file_path):
        return file_path
    else:
        root, ext = os.path.splitext(file_path)
        return get_unique_file_name(f"{root}_{uuid.uuid4().hex}{ext}")

def upload_video(cedula, id_audiencia, id_comparendo, file_path, bucket_name, object_name):
    file_name = f'{cedula}_{id_audiencia}_{id_comparendo}.mp4'
    file_name = get_unique_file_name(file_name)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_url = None
    try:
        s3.save(file_name, open(file_path, 'rb'))
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{file_name}'
        print(f"Video cargado exitosamente a AWS S3: {s3_url}")
    except Exception as e:
        print(f"Error al cargar el video a S3: {str(e)}")
        raise ValueError(f"Error al cargar el video a S3: {str(e)}")
    return s3_url

