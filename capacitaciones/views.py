from django.shortcuts import render
from .models import Playlist, Video
from django.shortcuts import get_object_or_404

def index(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, 'capacitaciones/index.html', context)

def videoTutorial(request, video_id):
    video = get_object_or_404(Video, id=video_id)
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
