from django import forms
from .models import Page

# Formulario para crear y editar páginas de contenido
class PageForm(forms.ModelForm):

    class Meta:
        model = Page  # Modelo asociado al formulario
        fields = ['title', 'content', 'order']  # Campos que se mostrarán en el formulario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),      # Widget para el título
            'content': forms.Textarea(attrs={'class': 'form-control'}),     # Widget para el contenido
            'order': forms.NumberInput(attrs={'class': 'form-control'}),    # Widget para el orden
        }