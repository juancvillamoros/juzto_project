from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Video(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

