from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, related_name="mensaje_remitente", on_delete=models.CASCADE)
    receptor   = models.ForeignKey(User, related_name="mensaje_receptor", on_delete=models.CASCADE)
    contenido  = models.TextField()
    fecha      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remitente.username} → {self.receptor.username}"
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="fotos_perfil/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    area_trabajo = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    nivel_estudio = models.TextField(blank=True, null=True, help_text="Ej: Licenciatura en Ingeniería, Diplomado en Python")
    idiomas = models.TextField(blank=True, null=True, help_text="Ej: Español (Nativo), Inglés (B2)")
    conocimientos = models.TextField(blank=True, null=True, help_text="Ej: Python, JavaScript, Django, React, SQL")

    def __str__(self):
        return self.user.username

class Conocimiento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Experiencia(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    proyecto = models.CharField(max_length=200)
    rol = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.proyecto} - {self.rol}"
    
# --- GESTIÓN DE PROYECTOS Y ROLES ---
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    lider = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default="pendiente")
    descripcion = models.TextField(blank=True, null=True)
    dificultad = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    participantes = models.ManyToManyField(User, related_name="proyectos_participante", blank=True)
    # Límite de miembros que permite el proyecto (0 = sin límite)
    limite_miembros = models.PositiveIntegerField(default=0)
    # Porcentaje de avance del proyecto (0-100)
    progreso = models.PositiveIntegerField(default=0)
    # Nuevos campos: habilidades y lenguajes requeridos
    habilidades_requeridas = models.TextField(blank=True, null=True, help_text="Ej: Liderazgo, Comunicación, Pensamiento crítico")
    lenguajes_programacion = models.TextField(blank=True, null=True, help_text="Ej: Python, JavaScript, SQL")

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

# --- GESTIÓN DE TAREAS ---
class Tarea(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')]
    ESTADOS_RETRASO = [('a_tiempo', 'A tiempo'), ('en_retraso', 'En retraso'), ('entregado_tarde', 'Entregado tarde')]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción detallada de la actividad")
    asignado_a = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    archivo_evidencia = models.FileField(upload_to='evidencias_tareas/', blank=True, null=True, help_text="PDF, imagen o archivo comprimido como evidencia")
    completado_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tareas_completadas')
    fecha_completado = models.DateTimeField(null=True, blank=True)
    # Nuevos campos: fecha de entrega y estado de retraso
    fecha_asignacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora límite de entrega")
    estado_retraso = models.CharField(max_length=20, choices=ESTADOS_RETRASO, default='a_tiempo')
    
    def get_dias_restantes(self):
        """Retorna los días restantes hasta la fecha de entrega"""
        from django.utils import timezone
        ahora = timezone.now()
        if self.estado == 'completada':
            return None
        if not self.fecha_entrega:
            return None
        dias = (self.fecha_entrega - ahora).days
        return max(dias, 0)
    
    def get_estado_visual(self):
        """Retorna el estado visual: a_tiempo, en_retraso, entregado_tarde"""
        from django.utils import timezone
        ahora = timezone.now()
        
        if self.estado == 'completada':
            # Si fue entregado después de la fecha
            if self.fecha_completado and self.fecha_entrega and self.fecha_completado > self.fecha_entrega:
                return 'entregado_tarde'
            return 'a_tiempo'
        else:
            # Si la fecha ya pasó pero no está completada
            if self.fecha_entrega and ahora > self.fecha_entrega:
                return 'en_retraso'
            return 'a_tiempo'

# --- INSIGNIAS Y GAMIFICACIÓN ---
class Insignia(models.Model):
    # usuario: opcionalmente quién creó la insignia
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    puntos = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='insignias/', blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    
class InsigniaOtorgada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="insignias")
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True) # Opcional: "Por excelente liderazgo"

    def __str__(self):
        return f"{self.insignia.nombre} -> {self.usuario.username}"

# --- EXÁMENES (Simplificado) ---

class Examen(models.Model):
    titulo = models.CharField(max_length=200)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="examenes")
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    TIPOS = [('opcion_multiple', 'Opción Múltiple'), ('verdadero_falso', 'Verdadero / Falso')]
    
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name="preguntas")
    texto_pregunta = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='opcion_multiple')
    
    # Para simplificar, guardamos las opciones como texto separado por comas si es necesario
    # O idealmente crearíamos otro modelo "Opcion", pero esto basta para el prototipo
    opcion_correcta = models.CharField(max_length=200) 
    otras_opciones = models.TextField(help_text="Separa las opciones incorrectas con comas")

    def __str__(self):
        return self.texto_pregunta
    

class ResultadoExamen(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    puntaje = models.FloatField() # Ej: 80.0
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.examen.titulo}: {self.puntaje}"
    
class ComentarioProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} en {self.proyecto.nombre}"


class ProyectoActividad(models.Model):
    """
    Historial de acciones relacionadas a un proyecto (tareas, cambios de estado, participantes, etc.).
    """
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='actividad')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=100)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        who = self.usuario.username if self.usuario else 'Sistema'
        return f"{self.fecha} — {who}: {self.accion}"