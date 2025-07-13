from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from .models import Profile


# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'  

    def get_success_url(self):
        return reverse_lazy('login') +'?register' # Redireccionar a la página de inicio de sesión después del registro exitoso
    
    def get_form(self, form_class = None):
        form =super(SignUpView, self).get_form()
        #Se modificara el formulario en tiempo real
        form.fields['username'].widget= forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario'})
        form.fields['password1'].widget= forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        form.fields['password2'].widget= forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Repita la contraseña'})
        
        return form
    
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = Profile
    fields =['avatar','bio', 'link']
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        #Recuperar el  objeto que se va editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
        