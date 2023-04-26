import requests
from django.conf import settings
from typing import Dict, Any
from ..models import Video


class ZohoApiClient:
    """A client for the Zoho API."""

    def __init__(self):
        self.api_uri = settings.ZOHO_API_URL
        self.auth_token = settings.ZOHO_AUTH_TOKEN

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.auth_token}'}

    def get_audiencia_by_id(self, id_audiencia: str) -> Dict[str, Any]:
        """Get the audiencia data for the specified ID."""
        headers = self._get_headers()
        api_url = f'{self.api_uri}/audiencias/{id_audiencia}'
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_audiencia_field(self, id_audiencia: str, field_name: str, field_value: Any) -> None:
        """Update the specified field for the audiencia with the specified ID."""
        headers = self._get_headers()
        headers['Content-Type'] = 'application/json'
        api_url = f'{self.api_uri}/audiencias/{id_audiencia}'
        data = {field_name: field_value}
        response = requests.put(api_url, headers=headers, json=data)
        response.raise_for_status()

    def add_video_to_audiencia(self, id_audiencia: str) -> None:
        """Add a video URL to the audiencia with the specified ID."""
        audiencia = self.get_audiencia_by_id(id_audiencia)
        if not audiencia:
            raise ValueError(f"Audiencia {id_audiencia} does not exist in Zoho")
        try:
            # Get the Video object with the unique_video_url.
            video = Video.objects.get(video_url__endswith=f"_{audiencia['user']}")
            video_url = video.video_url
        except Video.DoesNotExist:
            raise ValueError(f"Video URL not found for audiencia {id_audiencia}")
        self.update_audiencia_field(id_audiencia, 'url', video_url)
        print(f"Video URL added to audiencia {id_audiencia}")

    def add_audiencia(self, cedula: str, id_audiencia: str, id_comparendo: str,video_url: str) -> None:
        """Add a new audiencia to Zoho with the specified information."""
        headers = self._get_headers()
        headers['Content-Type'] = 'application/json'
        api_url = f'{self.api_uri}/audiencias'
        data = {
            'cedula': cedula,
            'id_audiencia': id_audiencia,
            'id_comparendo': id_comparendo,
            'url': video_url
        }
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Audiencia {id_audiencia} added to Zoho")

    def handle_zoho_error(self, error: Exception) -> None:
        """Handle a Zoho API error by raising a ValueError with a message."""
        if isinstance(error, requests.exceptions.HTTPError):
            error_msg = f"Zoho API returned error: {error.response.status_code} - {error.response.text}"
        else:
            error_msg = f"Error connecting to Zoho API: {str(error)}"
        print(error_msg)

