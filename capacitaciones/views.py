from django.shortcuts import render
from .models import Playlist, Video

def index(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, 'capacitaciones/index.html', context)

def video(request, video_id):
    video = Video.objects.get(id=video_id)
    playlist = video.playlist
    videos = playlist.videos.all()

    try:
        index = list(videos).index(video)
        if index > 0:
            previous = videos[index - 1]
        else:
            previous = None
        if index < len(videos) - 1:
            next = videos[index + 1]
        else:
            next = None
    except ValueError:
        previous = None
        next = None

    context = {
        'video': video,
        'previous': previous,
        'next': next,
    }

    return render(request, 'capacitaciones/video.html', context)
