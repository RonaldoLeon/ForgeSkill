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

    # AQUI FALTABA
    conocimientos = models.ManyToManyField("Conocimiento", blank=True)

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
    participantes = models.ManyToManyField(User, related_name="proyectos_participante", blank=True)

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
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    asignado_a = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

# --- INSIGNIAS Y GAMIFICACIÓN ---
class Insignia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
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