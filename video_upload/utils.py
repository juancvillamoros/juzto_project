from typing import Optional
from .models import Video
from .helpers.s3_helpers import upload_video
from django.contrib.auth.models import User



def upload_video_to_s3(file_path: str, cedula: str, id_audiencia: str, id_comparendo: str, bucket_name, object_name) -> str:
    """Upload a video file to S3 and return the URL."""
    s3_url = upload_video(cedula, id_audiencia, id_comparendo, file_path, bucket_name, object_name)
    return s3_url


def save_video_and_upload_to_s3(user_id: User, cedula: str, id_audiencia: str, id_comparendo: str, file_path: str, bucket_name: str, object_name: Optional[str] = None) -> str:
    """Save a video to the database and upload it to S3, returning the URL."""
    s3_url = upload_video_to_s3(file_path, cedula, id_audiencia, id_comparendo, bucket_name, object_name)
    unique_video_url = f"{s3_url}_{user_id}"
    try:
        # Check if the Video object already exists with the same unique_video_url.
        Video.objects.get(video_url=unique_video_url)
        raise ValueError(f"Video URL already exists for audiencia {id_audiencia}")
    except Video.DoesNotExist:
        # If the Video object does not exist, create a new one with the unique_video_url.
        video = Video(
            user_id=user_id,
            cedula=cedula,
            id_audiencia=id_audiencia,
            id_comparendo=id_comparendo,
            video_url=unique_video_url
        )
        video.save()
    return unique_video_url






