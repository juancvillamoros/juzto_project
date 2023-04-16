from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import os


class Reporte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=None)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"

    def validate_file_size(value):
        filesize = value.size
        if filesize > 10485760:
            raise ValidationError("El archivo no puede ser mayor a 10MB.")
    
    def validate_file_extension(value):
        
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
        if not ext.lower() in valid_extensions:
            raise ValidationError("Tipo de archivo no soportado. Los formatos soportados son: pdf, doc, docx, xls, xlsx.")
    
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True, validators=[validate_file_size, validate_file_extension])
    
