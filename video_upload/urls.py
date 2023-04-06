from django.urls import path
from . import views

app_name = 'video_upload'

urlpatterns = [
    path('videos/subir/', views.upload_video, name='upload_video'),
    path('videos/lista/', views.video_list, name='video_list'),
]
