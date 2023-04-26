from django.db import models
from django.contrib.auth.models import User


class Reporte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    archivo = models.ImageField(upload_to='bugs/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"Reporte de {self.user.username}"



