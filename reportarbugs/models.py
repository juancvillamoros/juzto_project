from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"
