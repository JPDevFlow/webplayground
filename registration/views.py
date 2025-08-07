from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from .models import Profile

# Vistas para el registro y actualización de perfil de usuario

class SignUpView(CreateView):
    # Vista para el registro de nuevos usuarios
    form_class = UserCreationForm
    template_name = 'registration/signup.html'  # Plantilla a utilizar

    def get_success_url(self):
        # Redireccionar a la página de inicio de sesión después del registro exitoso
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class = None):
        # Personaliza los widgets de los campos del formulario en tiempo real
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre de usuario'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Repita la contraseña'})
        return form

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    # Vista para actualizar el perfil del usuario
    form_class = ProfileForm
    success_url = reverse_lazy('profile')  # Redireccionar al perfil tras actualizar
    template_name = 'registration/profile_form.html'  # Plantilla a utilizar

    def get_object(self):
        # Recuperar el objeto Profile que se va a editar, lo crea si no existe
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    # Vista para actualizar el email del usuario
    form_class = EmailForm
    success_url = reverse_lazy('profile')  # Redireccionar al perfil tras actualizar
    template_name = 'registration/profile_email_form.html'  # Plantilla a utilizar

    def get_object(self):
        # Recuperar el objeto User que se va a editar (el usuario actual)
        return self.request.user
    
    def get_form(self, form_class=None):
        # Personaliza el widget del campo email en tiempo real
        form = super(EmailUpdate, self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'})
        return form