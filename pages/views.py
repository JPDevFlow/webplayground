from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Page
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import PageForm

class StaffRequiredMixin(object):
    """
    Mixin para requerir que el usuario sea miembro del staff.
    Se agrega el decorador staff_member_required para asegurar que solo los miembros del staff
    puedan acceder a las vistas que hereden de este mixin.
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

# Vista para listar todas las páginas
class PageListView(ListView):
    model = Page

# Vista para mostrar el detalle de una página
class PageDetailView(DetailView):
    model = Page

# Vista para crear una nueva página (solo staff)
@method_decorator(staff_member_required, name='dispatch')
class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy("pages:pages")  # Redirige al listado de páginas tras crear

# Vista para actualizar una página existente (solo staff)
@method_decorator(staff_member_required, name='dispatch')
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = "_update_form"  # Sufijo para el template de actualización

    def get_success_url(self):
        # Redirige a la misma página de edición con un parámetro de éxito
        return reverse_lazy("pages:update", args=[self.object.id]) + '?ok'

# Vista para eliminar una página (solo staff)
@method_decorator(staff_member_required, name='dispatch')
class PageDeleteView(DeleteView):
    model = Page
    success_url = reverse_lazy("pages:pages")  # Redirige al listado

