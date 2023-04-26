from django.contrib.auth.models import User
from ..models import Video
from .s3_helpers import upload_video
from django.conf import settings
import requests


def add_video_to_zoho(video_url: str, cedula: str, id_audiencia: str, id_comparendo: str, user: User):
    """Add video data to Zoho using Deluge API."""
    # Define API endpoint and parameters
    endpoint = settings.ZOHO_API_URL
    params = {
        "workflow": "Add_Video_Data",
        "criteria": f"cedula == {cedula} and id_audiencia == {id_audiencia} and id_comparendo == {id_comparendo}",
        "video_url": video_url,
        "cedula": cedula,
        "id_audiencia": id_audiencia,
        "id_comparendo": id_comparendo,
        "user_id": user.id,
        "auth_type": "apikey",
        "apikey": settings.ZOHO_AUTH_TOKEN
    }
    
    # Send API request and handle response
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error adding video to Zoho: {str(e)}")
    
    result = response.json()
    if result["response"]["status"] != "success":
        raise ValueError(f"Error adding video to Zoho: {result['response']['message']}")
    print(f"Video added to Zoho: {result['response']['data']['id']}")
        

def save_video_to_db(user: User, cedula: str, id_audiencia: str, id_comparendo: str, file_path: str) -> str:
    """Compress, upload, and save the video link to the database."""
    # Upload file to S3 and get URL
    s3_url = upload_video(file_path, user, cedula, id_audiencia, id_comparendo)
    
    # Generate unique video URL with user ID
    unique_video_url = f"{s3_url}_{user.id}"
    
    if not unique_video_url:
        raise ValueError("Failed to generate unique video URL.")
    
    if Video.objects.filter(video_url=unique_video_url).exists():
        raise ValueError(f"Video URL already exists for audiencia {id_audiencia}")
    
    # If the Video object does not exist, create a new one with the unique_video_url
    video = Video(
        user=user,
        cedula=cedula,
        id_audiencia=id_audiencia,
        id_comparendo=id_comparendo,
        video_url=unique_video_url
    )
    video.save()
        
    # Add video data to Zoho
    add_video_to_zoho(unique_video_url, cedula, id_audiencia, id_comparendo, user)
        
    return unique_video_url
