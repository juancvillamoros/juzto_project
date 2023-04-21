from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    cedula = models.CharField(max_length=255, validators=[RegexValidator(regex='^[0-9]{10}$', message='Cedula invalida')])
    id_audiencia = models.CharField(max_length=255, validators=[RegexValidator(regex='^[0-9]{10}$', message='audiencia invalida')])
    id_comparendo = models.CharField(max_length=255, validators=[RegexValidator(regex='^[0-9]{10}$', message='comparendo invalida')])
    video_url = models.SlugField(unique=True, max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cedula} - {self.id_audiencia} - {self.id_comparendo}'
