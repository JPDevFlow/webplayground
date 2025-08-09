from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Modelo para los mensajes individuales
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que envía el mensaje
    content = models.TextField()  # Contenido del mensaje
    created = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación

    class Meta:
        ordering = ['-created']  # Ordenar mensajes del más reciente al más antiguo

# Manager personalizado para el modelo Thread
class ThreadManager(models.Manager):
    # Buscar un hilo entre dos usuarios
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0]
        return None

    # Buscar o crear un hilo entre dos usuarios
    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread

# Modelo para los hilos de conversación
class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')  # Usuarios participantes en el hilo
    messages = models.ManyToManyField(Message)  # Mensajes del hilo
    updated = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    objects = ThreadManager()  # Usar el manager personalizado

    class Meta:
        ordering = ['-updated']  # Ordenar hilos por última actualización descendente

# Señal para controlar los cambios en la relación muchos a muchos de mensajes en un hilo
def message_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)  # Instancia del hilo
    action = kwargs.pop('action', None)      # Acción realizada
    pk_set = kwargs.pop('pk_set', None)      # Conjunto de claves primarias de mensajes afectados
    print(instance, action, pk_set)
    false_pk_set = set()
    if action == 'pre_add':
        # Verificar que los usuarios de los mensajes pertenezcan al hilo
        for msg_pk in pk_set and pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print(f'upps!, {msg.user} no forma parte del hilo')
                false_pk_set.add(msg_pk)
    pk_set.difference_update(false_pk_set)

    # Forzar la actualización del hilo
    instance.save()

# Conectar la señal al modelo Thread para la relación messages
m2m_changed.connect(message_changed, sender=Thread.messages.through)