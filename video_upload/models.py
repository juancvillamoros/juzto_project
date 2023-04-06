from django.db import models

# Create your models here.
class Video(models.Model):
    cedula = models.CharField(max_length=255)
    id_audiencia = models.CharField(max_length=255)
    id_comparendo = models.CharField(max_length=255)
    video = models.URLField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cedula} - {self.id_audiencia} - {self.id_comparendo}'