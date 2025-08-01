from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
# Create your views here.

@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'
    

@method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404("No tienes los permisos necesarios para ver este hilo.")
        return obj
    

@login_required
def add_message(request, pk):
    json_response = {'created': False}
    content = request.GET.get('content', None)
    
    if content:
        thread = Thread.objects.filter(pk=pk).first()
        if thread and request.user in thread.users.all():
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            # Si es el primer mensaje del hilo
            if thread.messages.count() == 1:
                json_response['first'] = True
    return JsonResponse(json_response)