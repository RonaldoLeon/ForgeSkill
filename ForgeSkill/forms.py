from django import forms
from .models import Perfil, Experiencia, Conocimiento
from .models import Tarea
from django.contrib.auth.models import User
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'dificultad', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Nombre del proyecto'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 3}),
            'dificultad': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Baja/Media/Alta'}),
        }

class PerfilForm(forms.ModelForm):
    conocimientos = forms.ModelMultipleChoiceField(
        queryset=Conocimiento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Perfil
        fields = ['foto', 'bio', 'area_trabajo', 'telefono', 'ciudad']
        
class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['proyecto', 'rol', 'descripcion', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }


class TareaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('proyecto_id', None)
        super(TareaForm, self).__init__(*args, **kwargs)
        if proyecto_id:
            # Aquí podrías filtrar usuarios que SOLO pertenezcan al proyecto (si tuvieras esa lógica)
            # Por ahora mostramos todos los usuarios para simplificar
            self.fields['asignado_a'].queryset = User.objects.all()

    class Meta:
        model = Tarea
        fields = ['titulo', 'asignado_a', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Ej: Diseñar DB'}),
            'asignado_a': forms.Select(attrs={'class': 'input-estilo'}),
            'estado': forms.Select(attrs={'class': 'input-estilo'}),
        }

# En forms.py
from .models import Insignia, InsigniaOtorgada

class InsigniaForm(forms.ModelForm):
    class Meta:
        model = Insignia
        # El modelo `Insignia` sólo define `usuario`, `nombre` y `fecha`.
        # Mostramos únicamente `nombre` en el formulario de creación/edición.
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Ej: Liderazgo'}),
        }

class OtorgarInsigniaForm(forms.ModelForm):
    class Meta:
        model = InsigniaOtorgada
        fields = ['usuario', 'insignia', 'motivo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'input-estilo'}),
            'insignia': forms.Select(attrs={'class': 'input-estilo'}),
            'motivo': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 2, 'placeholder': 'Ej: Por ayudar a sus compañeros...'}),
        }