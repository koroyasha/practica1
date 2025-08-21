from django.db import models

class TextoAnalizado(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='analisis/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Texto analizado: {self.titulo[:50]}...'

# Create your models here.
