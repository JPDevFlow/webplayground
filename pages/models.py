from django.db import models
from ckeditor.fields import RichTextField

# Modelo para representar una página de contenido
class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)  # Título de la página
    content = RichTextField(verbose_name="Contenido")  # Contenido enriquecido de la página (usa CKEditor)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)  # Orden de aparición de la página
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")  # Fecha de creación
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")  # Fecha de última edición

    class Meta:
        verbose_name = "página"  # Nombre singular para el admin
        verbose_name_plural = "páginas"  # Nombre plural para el admin
        ordering = ['order', 'title']  # Orden por defecto: primero por orden, luego por título

    def __str__(self):
        return self.title  # Representación en texto de la página
