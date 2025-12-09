from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Mensaje
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Perfil, Experiencia
from .forms import PerfilForm, ExperienciaForm
from .forms import TareaForm
from .models import Tarea, Proyecto
from django.shortcuts import get_object_or_404
import random
from .forms import ProyectoForm
from django.views.decorators.http import require_POST
from .models import Examen, ResultadoExamen, Pregunta
from .models import Insignia, InsigniaOtorgada
from .forms import InsigniaForm, OtorgarInsigniaForm
from .models import ComentarioProyecto, Proyecto
from django.shortcuts import get_object_or_404, redirect
from .models import Solicitud, Proyecto
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('login')

def login_view(request):
    # Soporta POST desde la plantilla: campos `email` (que puede ser email o username) y `password`
    if request.method == 'POST':
        # El formulario envía `identifier` que puede ser email o username
        email_or_username = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '')

        # Intentar primero por username (campo obligatorio)
        user = authenticate(request, username=email_or_username, password=password)
        
        if user is None:
            # Si no funciona por username, intentar por email
            try:
                usuario_por_email = User.objects.get(email__iexact=email_or_username)
                user = authenticate(request, username=usuario_por_email.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            # Si el usuario es staff (admin), redirigir al panel Django admin
            if user.is_staff:
                return redirect('admin:index')
            else:
                return redirect('dashboard')
        else:
            # No se pudo autenticar
            messages.error(request, 'Email/Usuario o contraseña incorrectos. Verifica tus credenciales.')

    return render(request, 'login.html')
 
def home_view(request):
    return render(request, 'home.html')

def resitro_view(request):
    # Maneja registro desde la plantilla `registro.html`
    if request.method == 'POST':
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirmPassword', '')

        # Validaciones básicas
        if password != confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')
            return render(request, 'registro.html')

        # Usamos el email como username para simplificar
        username = email
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Crear perfil asociado (opcional si se crea en otra vista)
        try:
            Perfil.objects.create(user=user)
        except Exception:
            pass

        # Loguear al usuario automáticamente
        user_auth = authenticate(request, username=username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('dashboard')

        return redirect('login')

    return render(request, 'registro.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def recuperacion_view(request):
    return render(request, 'recuperacion.html')
 
def usuario_view(request):
    return render(request, 'usuario.html')

def dashboard_view(request):
    # Mostrar métricas personalizadas en el dashboard del usuario
    proyectos_activos = 0
    insignias_count = 0
    progreso_total = 0
    proyectos_recomendados = []
    catalogo_insignias = []

    if request.user.is_authenticated:
        # Proyectos donde el usuario participa
        proyectos_participando = Proyecto.objects.filter(participantes=request.user)
        proyectos_activos = proyectos_participando.count()

        # Insignias otorgadas al usuario
        insignias_count = InsigniaOtorgada.objects.filter(usuario=request.user).count()

        # Catálogo de insignias (todas) y marcar las que ya tiene el usuario
        todas_insignias = Insignia.objects.all()
        otorgadas_ids = set(InsigniaOtorgada.objects.filter(usuario=request.user).values_list('insignia_id', flat=True))
        catalogo_insignias = []
        for ins in todas_insignias:
            catalogo_insignias.append({
                'id': ins.id,
                'nombre': ins.nombre,
                'tiene': ins.id in otorgadas_ids,
            })

        # Calcular progreso total: promedio del % de tareas completadas en los proyectos donde participa
        porcentajes = []
        for p in proyectos_participando:
            tareas_total = Tarea.objects.filter(proyecto=p).count()
            tareas_completadas = Tarea.objects.filter(proyecto=p, estado='completada').count()
            if tareas_total > 0:
                porcentajes.append((tareas_completadas / tareas_total) * 100)
            else:
                # Si no hay tareas, consideramos 0% de progreso
                porcentajes.append(0)

        if porcentajes:
            progreso_total = int(sum(porcentajes) / len(porcentajes))
        else:
            progreso_total = 0

        # Proyectos recomendados: proyectos cuyo líder es staff (creados por admins) y aprobados
        proyectos_recomendados = Proyecto.objects.filter(lider__is_staff=True, estado='aprobada')[:6]

    return render(request, 'dashboard.html', {
        'proyectos_activos': proyectos_activos,
        'insignias_count': insignias_count,
        'progreso_total': progreso_total,
        'proyectos_recomendados': proyectos_recomendados,
        'catalogo_insignias': catalogo_insignias,
    })

def proyectos_list(request):
    # Mostrar solo proyectos aprobados para usuarios normales
    proyectos = Proyecto.objects.filter(estado='aprobada')
    categorias = list(proyectos.values_list('dificultad', flat=True).distinct())
    
    # Indicar cuáles proyectos el usuario ya está participando
    usuario_participante = set()
    if request.user.is_authenticated:
        usuario_participante = set(
            Proyecto.objects.filter(
                participantes=request.user
            ).values_list('id', flat=True)
        )

    # IDs de proyectos a los que el usuario ya aplicó
    aplicado_ids = set()
    if request.user.is_authenticated:
        from .models import Solicitud
        aplicado_ids = set(Solicitud.objects.filter(usuario=request.user).values_list('proyecto_id', flat=True))

    # Pasar proyectos también como queryset para templates donde sea necesario
    
    return render(request, 'proyectos_list.html', {
        'proyectos': proyectos, 
        'categorias': categorias,
        'usuario_participante': usuario_participante
        , 'aplicado_ids': aplicado_ids
    })
 
# Reemplaza tu actual proyecto_detalle con esto:
def proyecto_detalle(request, proyecto_id=None): # Acepta un ID opcionalmente
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    else:
        # Solo para pruebas si entras sin ID, agarramos el primero que exista
        proyecto = Proyecto.objects.first() 
    
    return render(request, 'proyecto_detalle.html', {'proyecto': proyecto})
 
def mis_proyectos(request):
    # Mostrar proyectos donde el usuario participa (incluye los que lidera)
    from django.db.models import Q
    proyectos = Proyecto.objects.filter(Q(participantes=request.user) | Q(lider=request.user)).distinct()

    # IDs de proyectos en los que el usuario participa
    usuario_participante = set()
    if request.user.is_authenticated:
        usuario_participante = set(
            Proyecto.objects.filter(participantes=request.user).values_list('id', flat=True)
        )

    # Postulaciones del usuario
    solicitudes = Solicitud.objects.filter(usuario=request.user).select_related('proyecto') if request.user.is_authenticated else []

    aplicado_ids = set()
    if request.user.is_authenticated:
        aplicado_ids = set(solicitudes.values_list('proyecto_id', flat=True))

    return render(request, 'mis_proyectos.html', {
        'proyectos': proyectos,
        'usuario_participante': usuario_participante,
        'aplicado_ids': aplicado_ids,
        'solicitudes': solicitudes,
    })

@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            perfil.conocimientos.set(form.cleaned_data['conocimientos'])
            return redirect("perfil")

    else:
        form = PerfilForm(instance=perfil)

    experiencias = Experiencia.objects.filter(perfil=perfil)

    return render(request, "profile.html", {
        "form": form,
        "perfil": perfil,
        "experiencias": experiencias,
    })

def admin_panel(request):

    usuarios_totales = User.objects.count()
    proyectos_activos = Proyecto.objects.filter(estado="aprobado").count()
    insignias_dadas = Insignia.objects.count()

    usuarios_qs = User.objects.all().order_by("-date_joined")[:10]
    proyectos_pendientes = Proyecto.objects.filter(estado="pendiente")
    proyectos_all = Proyecto.objects.all()

    usuarios = []
    for u in usuarios_qs:
        usuarios.append({
            'id': u.id,
            'username': u.username,
            'rol': 'Admin' if u.is_staff else 'Usuario',
            'estado': 'Activo' if u.is_active else 'Bloqueado',
            'is_active': u.is_active,
            'is_staff': u.is_staff,
        })

    return render(request, 'admin_panel.html', {
        "stats": {
            "usuarios_totales": usuarios_totales,
            "proyectos_activos": proyectos_activos,
            "insignias_dadas": insignias_dadas
        },
        "usuarios": usuarios,
        "proyectos_pendientes": proyectos_pendientes,
        "proyectos_all": proyectos_all,
    })


@login_required
@require_POST
def approve_project(request, proyecto_id):
    p = get_object_or_404(Proyecto, id=proyecto_id)
    p.estado = 'aprobada'
    p.save()
    return redirect('admin_panel')


@login_required
@require_POST
def reject_project(request, proyecto_id):
    p = get_object_or_404(Proyecto, id=proyecto_id)
    p.estado = 'rechazada'
    p.save()
    return redirect('admin_panel')


@login_required
def join_project(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.participantes.add(request.user)
    return redirect('proyectos_list')


@login_required
def leave_project(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.participantes.remove(request.user)
    return redirect('proyectos_list')

@login_required
def agregar_experiencia(request):
    perfil = Perfil.objects.get(user=request.user)

    if request.method == "POST":
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.perfil = perfil
            exp.save()
            return redirect("perfil")

    else:
        form = ExperienciaForm()

    return render(request, "agregar_experiencia.html", {"form": form})


@login_required
def crear_proyecto(request):
    # Solo usuarios staff (admins) pueden crear proyectos
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para crear proyectos.')
        return redirect('proyectos_list')

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.lider = request.user
            proyecto.estado = 'pendiente'
            proyecto.save()
            # If imagen was uploaded, save m2m or file already handled by ModelForm
            return redirect('mis_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})


@login_required
@require_POST
def block_user(request, user_id):
    # Alterna el estado is_active del usuario (bloquear/desbloquear)
    u = get_object_or_404(User, id=user_id)
    if u != request.user:
        u.is_active = not u.is_active
        u.save()
    return redirect('admin_panel')


@login_required
@require_POST
def change_role(request, user_id):
    # Cambia entre 'Usuario' y 'Staff' simplificado (is_staff)
    u = get_object_or_404(User, id=user_id)
    if u != request.user:
        u.is_staff = not u.is_staff
        u.save()
    return redirect('admin_panel')


@login_required
@require_POST
def admin_delete_proyecto(request, proyecto_id):
    # Solo staff puede borrar proyectos desde el panel
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar proyectos.')
        return redirect('admin_panel')

    p = Proyecto.objects.filter(id=proyecto_id).first()
    if not p:
        messages.error(request, 'El proyecto no existe o ya fue eliminado.')
        return redirect('admin_panel')
    # Eliminar archivo de imagen asociado si existe (usa el storage backend)
    try:
        if p.imagen:
            p.imagen.delete(save=False)
    except Exception:
        # No bloquear por errores de borrado de archivo
        pass

    p.delete()
    messages.success(request, 'Proyecto eliminado correctamente.')
    return redirect('admin_panel')

@login_required
def generar_pdf(request):
    perfil = Perfil.objects.get(user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 760, f"CV - {perfil.user.first_name} {perfil.user.last_name}")

    p.setFont("Helvetica", 12)
    y = 720

    # Bio
    p.drawString(50, y, "Bio:")
    y -= 20
    p.drawString(60, y, perfil.bio or "No registrada")

    # Área
    y -= 30
    p.drawString(50, y, f"Área profesional: {perfil.area_trabajo}")

    # Conocimientos
    y -= 40
    p.drawString(50, y, "Conocimientos:")
    for c in perfil.conocimientos.all():
        y -= 20
        p.drawString(60, y, f"- {c.nombre}")

    # Experiencia
    y -= 40
    p.drawString(50, y, "Experiencia:")
    experiencias = Experiencia.objects.filter(perfil=perfil)
    for e in experiencias:
        y -= 20
        p.drawString(60, y, f"{e.proyecto} — {e.rol} ({e.fecha})")

    p.showPage()
    p.save()

    return response

@login_required
def notificaciones(request):
    usuarios = User.objects.exclude(id=request.user.id)
    return render(request, "notificaciones.html", {"usuarios": usuarios})

@login_required
def chat(request, user_id):
    otro = User.objects.get(id=user_id)

    if request.method == "POST":
        contenido = request.POST.get("mensaje")
        if contenido.strip() != "":
            Mensaje.objects.create(
                remitente=request.user,
                receptor=otro,
                contenido=contenido
            )
        return redirect(f"/chat/{user_id}/")

    mensajes = Mensaje.objects.filter(
        remitente__in=[request.user, otro],
        receptor__in=[request.user, otro]
    ).order_by("fecha")

    return render(request, "chat.html", {
        "otro": otro,
        "mensajes": mensajes
    })


@login_required
def chats_list(request):
    # Buscar término (q) para filtrar usuarios
    q = request.GET.get('q', '').strip()

    # Usuarios con los que ya hay mensajes
    mensajes = Mensaje.objects.filter(Q(remitente=request.user) | Q(receptor=request.user))
    user_ids = set()
    for m in mensajes:
        if m.remitente and m.remitente != request.user:
            user_ids.add(m.remitente.id)
        if m.receptor and m.receptor != request.user:
            user_ids.add(m.receptor.id)

    chats_users = User.objects.filter(id__in=user_ids)

    # Resultado de búsqueda (puede listar todos si q está vacío)
    if q:
        search_users = User.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        ).exclude(id=request.user.id)
    else:
        search_users = User.objects.exclude(id=request.user.id)[:50]

    return render(request, 'chats_list.html', {
        'chats_users': chats_users,
        'search_users': search_users,
        'q': q,
    })

# --- VISTAS MENTOR / LIDER DE PROYECTO ---

@login_required
def gestion_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Solo el líder del proyecto o staff puede gestionar
    if request.user != proyecto.lider and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para gestionar este proyecto.')
        return redirect('dashboard')

    # Solicitudes pendientes para este proyecto
    solicitudes = Solicitud.objects.filter(proyecto=proyecto).order_by('-id')

    # Tareas reales del proyecto
    tareas = Tarea.objects.filter(proyecto=proyecto)

    # Participantes
    participantes = proyecto.participantes.all()

    return render(request, 'mentor/dashboard_proyecto.html', {
        'proyecto': proyecto,
        'solicitudes': solicitudes,
        'tareas': tareas,
        'participantes': participantes,
    })


@login_required
@require_POST
def approve_solicitud(request, solicitud_id):
    s = get_object_or_404(Solicitud, id=solicitud_id)
    proyecto = s.proyecto
    # Only leader or staff can approve
    if request.user != proyecto.lider and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para aprobar esta solicitud.')
        return redirect('gestion_proyecto', proyecto_id=proyecto.id)

    s.estado = 'aprobada'
    s.save()
    # Añadir al participante
    proyecto.participantes.add(s.usuario)

    # Enviar notificación por correo (si es posible)
    try:
        subject = f"Tu postulación a {proyecto.nombre} fue aprobada"
        body = f"Hola {s.usuario.first_name or s.usuario.username},\n\nTu postulación al proyecto '{proyecto.nombre}' ha sido aprobada. Puedes acceder al proyecto en la plataforma.\n\nSaludos,\nEquipo ForgeSkill"
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'no-reply@forgeskill.local'
        send_mail(subject, body, from_email, [s.usuario.email], fail_silently=True)
    except Exception:
        pass

    messages.success(request, f"Se aprobó la postulación de {s.usuario.username}.")
    return redirect('gestion_proyecto', proyecto_id=proyecto.id)


@login_required
@require_POST
def reject_solicitud(request, solicitud_id):
    s = get_object_or_404(Solicitud, id=solicitud_id)
    proyecto = s.proyecto
    if request.user != proyecto.lider and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para rechazar esta solicitud.')
        return redirect('gestion_proyecto', proyecto_id=proyecto.id)

    s.estado = 'rechazada'
    s.save()

    messages.info(request, f"Se rechazó la postulación de {s.usuario.username}.")
    return redirect('gestion_proyecto', proyecto_id=proyecto.id)

@login_required
def otorgar_insignia(request):
    # Lógica para mostrar formulario de insignias
    return render(request, 'mentor/otorgar_insignia.html')

# --- VISTAS ADMIN GENERAL (SUPER ADMIN) ---

@login_required
def admin_dashboard(request):
#    # Estadísticas Globales
    stats = {
        "usuarios_totales": 150,
        "proyectos_activos": 12,
        "insignias_dadas": 340
    }
    
    usuarios_recientes = [
        {"id": 1, "username": "NuevoUser1", "rol": "Usuario", "estado": "Activo"},
        {"id": 2, "username": "Spammer", "rol": "Usuario", "estado": "Bloqueado"},
    ]

    proyectos_pendientes = [
        {"id": 5, "nombre": "App de IA", "lider": "Dr. Smith"},
    ]

    return render(request, 'admin/admin_panel.html', {
        "stats": stats,
        "usuarios": usuarios_recientes,
        "proyectos_pendientes": proyectos_pendientes
    })


@login_required
def crear_tarea(request, proyecto_id):
    # Obtenemos el proyecto (o simulamos uno si no hay DB aun)
    # proyecto = get_object_or_404(Proyecto, id=proyecto_id) 
    
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.proyecto_id = proyecto_id # Asignamos el proyecto manualmente
            tarea.save()
            return redirect('gestion_proyecto', proyecto_id=proyecto_id)
    else:
        form = TareaForm(proyecto_id=proyecto_id)

    return render(request, 'mentor/tarea_form.html', {'form': form, 'titulo': 'Nueva Tarea'})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('gestion_proyecto', proyecto_id=tarea.proyecto.id)
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'mentor/tarea_form.html', {'form': form, 'titulo': 'Editar Tarea'})

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    proyecto_id = tarea.proyecto.id
    tarea.delete()
    return redirect('gestion_proyecto', proyecto_id=proyecto_id)

@login_required
def lista_examenes(request, proyecto_id):
    # Simulación
    examenes = [
        {"id": 1, "titulo": "Examen Final Backend", "preguntas_count": 10},
        {"id": 2, "titulo": "Test de Conocimientos Git", "preguntas_count": 5},
    ]
    return render(request, 'mentor/examenes_list.html', {'examenes': examenes, 'proyecto_id': proyecto_id})

@login_required
def crear_pregunta(request, examen_id):
    # Aquí iría la lógica similar a crear_tarea pero para preguntas
    return render(request, 'mentor/crear_pregunta.html', {'examen_id': examen_id})


@login_required
def tomar_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    preguntas = list(examen.preguntas.all())
    
    if request.method == 'POST':
        puntaje_total = 0
        aciertos = 0
        
        for p in preguntas:
            # El name del input en HTML será "pregunta_ID"
            respuesta_usuario = request.POST.get(f'pregunta_{p.id}')
            
            if respuesta_usuario == p.opcion_correcta:
                aciertos += 1
        
        # Calcular porcentaje (0 a 100)
        if len(preguntas) > 0:
            nota = (aciertos / len(preguntas)) * 100
        else:
            nota = 0
            
        # Guardar resultado
        ResultadoExamen.objects.create(
            usuario=request.user,
            examen=examen,
            puntaje=nota
        )
        
        # Redirigir al dashboard o mostrar resultado (simplificado)
        return render(request, 'alumno/resultado_examen.html', {'examen': examen, 'nota': nota, 'aciertos': aciertos})

    # GET: Preparar el examen
    # Preparamos las preguntas con sus opciones mezcladas para el template
    datos_preguntas = []
    for p in preguntas:
        opciones = [p.opcion_correcta] + p.otras_opciones.split(',')
        random.shuffle(opciones) # Mezclar para que no sea obvia la respuesta
        datos_preguntas.append({
            'objeto': p,
            'opciones': opciones
        })

    return render(request, 'alumno/tomar_examen.html', {'examen': examen, 'preguntas': datos_preguntas})



# --- SUPER ADMIN: GESTIÓN DE INSIGNIAS ---
@login_required
def lista_insignias(request):
    insignias = Insignia.objects.all()
    
    if request.method == 'POST':
        form = InsigniaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_insignias')
    else:
        form = InsigniaForm()
        
    return render(request, 'admin/insignias_list.html', {'insignias': insignias, 'form': form})

# --- MENTOR: OTORGAR INSIGNIA ---
@login_required
def otorgar_insignia_mentor(request):
    # Idealmente filtraríamos usuarios del proyecto actual del mentor
    # Por ahora mostramos todos
    
    if request.method == 'POST':
        form = OtorgarInsigniaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # O volver al proyecto
    else:
        form = OtorgarInsigniaForm()
    
    return render(request, 'mentor/otorgar_insignia.html', {'form': form})

# --- USUARIO: VER MIS INSIGNIAS ---
# (Esto puede ir dentro de tu vista 'perfil', pero aquí te dejo como obtenerlas)
# insignias_usuario = InsigniaOtorgada.objects.filter(usuario=request.user)


@login_required
def foro_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Procesar nuevo mensaje
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            ComentarioProyecto.objects.create(
                proyecto=proyecto,
                usuario=request.user,
                contenido=contenido
            )
            # Redirigir a la misma página para evitar reenvío de formularios
            return redirect('foro_proyecto', proyecto_id=proyecto_id)

    # Obtener mensajes (ordenados del más antiguo al más nuevo)
    comentarios = proyecto.comentarios.all().order_by('fecha')

    return render(request, 'foro_proyecto.html', {
        'proyecto': proyecto,
        'comentarios': comentarios
    })


# ... (tus otras vistas) ...

@login_required
@require_POST
def postular(request, proyecto_id):
    # 1. Buscamos el proyecto
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # 2. Si el usuario ya es participante o es el líder, no puede postular
    if proyecto.lider == request.user or proyecto.participantes.filter(id=request.user.id).exists():
        messages.info(request, 'Ya formas parte de este proyecto o eres el líder.')
        return redirect('proyectos_list')

    # 3. Creamos la solicitud si no existe ya
    solicitud, created = Solicitud.objects.get_or_create(
        usuario=request.user,
        proyecto=proyecto
    )

    if created:
        messages.success(request, 'Tu postulación fue registrada.')
    else:
        messages.info(request, 'Ya te habías postulado a este proyecto.')

    # 4. Redirigimos al usuario a Mis Proyectos (donde verá su postulación)
    return redirect('mis_proyectos')


@login_required
@require_POST
def cancel_postulacion(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    try:
        s = Solicitud.objects.get(usuario=request.user, proyecto=proyecto)
        s.delete()
        messages.success(request, 'Tu postulación fue cancelada.')
    except Solicitud.DoesNotExist:
        messages.info(request, 'No existe la postulación.')
    return redirect('mis_proyectos')