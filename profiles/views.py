from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Profile


# Vistas para el manejo de perfiles de usuario

# Vista para listar todos los perfiles
class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'  # Plantilla para mostrar la lista de perfiles

# Vista para mostrar el detalle de un perfil específico
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'  # Plantilla para mostrar el detalle del perfil

    def get_object(self):
        # Obtiene el perfil según el nombre de usuario pasado en la URL
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
