from django.db import models
from django.contrib.auth.models import User
from django.db.models import m2m_changed

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']


class Thread(models.Model):
    user = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)


def message_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    print(instance, action, pk_set)
    false_pk_set = set()
    if action is 'pre_add':
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user  not in instance.user.all():
                print(f'upps!, {msg.user} no forma parte del hilo')
                false_pk_set.add(msg_pk)
    pk_set.diference_update(false_pk_set)


m2m_changed.connect(message_changed, sender=Thread.messages.through)