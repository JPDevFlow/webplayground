from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Función personalizada para la ruta de subida del avatar
def custom_upload_to(instance, filename):
    # Elimina el avatar anterior antes de guardar uno nuevo
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Modelo de perfil de usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con User
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)  # Imagen de perfil
    bio = models.TextField(null=True, blank=True)  # Biografía del usuario
    link = models.URLField(max_length=200, null=True, blank=True)  # Enlace personal

# Señal para crear automáticamente un perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        print("Se acaba de crear un usuario y su perfil enlazado.")