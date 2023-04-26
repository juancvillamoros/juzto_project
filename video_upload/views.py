from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .forms import VideoForm
from .utils import save_video_and_upload_to_s3
from .models import Video
from django.conf import settings


@csrf_protect
@login_required
def video_list(request):
    videos = Video.objects.filter(user=request.user)
    return render(request, 'video_list.html', {'videos': videos})


def save_video_to_db(user, cedula, id_audiencia, id_comparendo, s3_url):
    Video.objects.create(
        user=user,
        cedula=cedula,
        id_audiencia=id_audiencia,
        id_comparendo=id_comparendo,
        video_url=s3_url
    )


@csrf_protect
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']
            # Call the function to save and upload the video to S3
            unique_video_url = save_video_and_upload_to_s3(
                user_id=request.user.id,
                cedula=form.cleaned_data['cedula'],
                id_audiencia=form.cleaned_data['id_audiencia'],
                id_comparendo=form.cleaned_data['id_comparendo'],
                file_path=video.temporary_file_path(),
                bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
                object_name=video.name
            )
        return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})
