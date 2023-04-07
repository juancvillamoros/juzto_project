import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# Las credenciales se almacenarán en un archivo local.
"""
El archivo youtube_token_json es simplemente un archivo de almacenamiento 
en el que se guarda el token de acceso OAuth 2.0 de YouTube para que se 
pueda reutilizar en sesiones posteriores sin tener que volver a autenticarse
y autorizarse. 
Este archivo es generado automáticamente por el código si no existe, 
o si la autorización anterior ha expirado.
"""
TOKEN_FILE = 'youtube_token.json'

# ID de la lista de reproducción en la que se agregarán los videos.
PLAYLIST_ID = 'YOUR_PLAYLIST_ID'

# Alcance de la autorización OAuth.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


def get_authenticated_service():
    """Devuelve un objeto del servicio de la API de YouTube autenticado con las credenciales del usuario."""
    credentials = None
    if os.path.exists(TOKEN_FILE):
        # Cargando credenciales desde un archivo local si ya existen.
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not credentials or not credentials.valid:
        # Si no hay credenciales válidas, se solicita la autorización del usuario a través del flujo OAuth.
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        credentials = flow.run_local_server(port=0)

        # Guardando las credenciales en un archivo local para futuros usos.
        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(credentials.to_json())

    # Se devuelve un objeto del servicio de la API de YouTube autenticado con las credenciales del usuario.
    return build('youtube', 'v3', credentials=credentials)


def add_video_to_playlist(youtube, video_id):
    """Agrega un video con el ID de video proporcionado a la lista de reproducción con el ID de lista de reproducción proporcionado."""
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": PLAYLIST_ID,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response


def get_playlist_videos(api_key, playlist_ids):
    # Obtener las credenciales de autenticación
    credentials, _ = google.auth.default(
        scopes=['https://www.googleapis.com/auth/youtube.readonly'])

    # Crear el objeto de servicio de la API de YouTube
    youtube = build('youtube', 'v3', credentials=credentials,
                    developerKey=api_key)

    # Inicializar una lista para almacenar todos los videos
    all_videos = []

    # Iterar a través de las listas de reproducción y obtener los detalles de cada video
    for playlist_id in playlist_ids:
        # Obtener los detalles de la lista de reproducción
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()

        # Obtener los detalles de los videos en la lista de reproducción
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Iterar a través de los videos en la lista de reproducción
            for playlist_item in playlistitems_list_response['items']:
                video_id = playlist_item['snippet']['resourceId']['videoId']
                video_title = playlist_item['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'

                # Agregar el video a la lista de videos
                all_videos.append({
                    'title': video_title,
                    'url': video_url
                })

            # Obtener la siguiente página de videos, si la hay
            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    return all_videos


# Configuración de autenticación
# En este ejemplo, usamos un archivo de credenciales JSON almacenado en una variable de entorno
# pero también puedes autenticar de otras formas, como el flujo de autenticación OAuth 2.0
# de Google
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
creds = None
if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
    creds = Credentials.from_authorized_user_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes)

# Función para obtener las listas de reproducción privadas de YouTube


def get_private_playlists():
    try:
        # Creamos el objeto de servicio de la API de YouTube
        service = build('youtube', 'v3', credentials=creds)

        # Hacemos la llamada a la API de YouTube para obtener las listas de reproducción privadas del usuario
        response = service.playlists().list(
            part="id,snippet,status",
            mine=True,
            maxResults=50,  # Máximo de 50 resultados
            fields="items(id,snippet(title,description,publishedAt),status(publishAt))"
        ).execute()

        # Devolvemos la lista de reproducción privada
        return response['items']

    except HttpError as error:
        print(f'Error al obtener las listas de reproducción privadas: {error}')
        return None
