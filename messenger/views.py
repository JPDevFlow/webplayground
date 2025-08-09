from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User

# Vista para mostrar la lista de hilos de conversación
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'
    

# Vista para mostrar el detalle de un hilo de conversación
@method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        # Solo permite ver el hilo si el usuario pertenece a él
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404("No tienes los permisos necesarios para ver este hilo.")
        return obj
    


# Vista para añadir un mensaje a un hilo (usada por AJAX)
def add_message(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            # Si es el primer mensaje del hilo, marca la respuesta como 'first'
            if len(thread.messages.all()) == 1:
                json_response['first'] = True
    else:
        raise Http404("No tienes los permisos necesarios para ver este hilo.")
    
    
    return JsonResponse(json_response)

# Vista para iniciar un hilo de conversación con otro usuario
@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    # Busca o crea un hilo entre el usuario actual y el usuario destino
    thread = Thread.objects.find_or_create(user, request.user)
    
    # Redirige al detalle del hilo recién creado o encontrado
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))