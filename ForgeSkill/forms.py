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
    class Meta:
        model = Perfil
        fields = ['foto', 'bio', 'area_trabajo', 'telefono', 'ciudad', 'nivel_estudio', 'idiomas', 'conocimientos']
        widgets = {
            'conocimientos': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 3, 'placeholder': 'Ej: Python, JavaScript, Django, React, SQL'})
        }
        
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
        fields = ['titulo', 'descripcion', 'asignado_a', 'fecha_entrega', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Ej: Diseñar DB'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 3, 'placeholder': 'Descripción detallada de la actividad'}),
            'asignado_a': forms.Select(attrs={'class': 'input-estilo'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'class': 'input-estilo', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'input-estilo'}),
        }

# En forms.py
from .models import Insignia, InsigniaOtorgada

class InsigniaForm(forms.ModelForm):
    class Meta:
        model = Insignia
        # Mostrar campos útiles para la creación de insignias
        fields = ['nombre', 'descripcion', 'puntos', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-estilo', 'placeholder': 'Ej: Liderazgo'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 2, 'placeholder': 'Descripción breve'}),
            'puntos': forms.NumberInput(attrs={'class': 'input-estilo', 'min': 0}),
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

class CompletarTareaForm(forms.Form):
    """Formulario para completar una tarea con evidencia"""
    archivo_evidencia = forms.FileField(
        label="Archivo de evidencia",
        help_text="PDF, imagen o archivo comprimido (máx 10MB)",
        required=True,
        widget=forms.FileInput(attrs={'class': 'input-estilo', 'accept': '.pdf,.jpg,.jpeg,.png,.zip,.rar'})
    )