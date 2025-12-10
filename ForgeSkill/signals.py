from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Tarea, Solicitud, InsigniaOtorgada, ProyectoActividad, Proyecto
from django.contrib.auth.models import User

@receiver(post_save, sender=Tarea)
def tarea_saved(sender, instance, created, **kwargs):
    proyecto = instance.proyecto
    usuario = None
    # Try to get user from kwargs if passed (some views might pass "user" in save)
    # Fall back to None (system) if not available
    accion = ''
    detalle = ''
    if created:
        accion = 'Tarea creada'
        detalle = f"Tarea '{instance.titulo}' creada."
    else:
        accion = 'Tarea actualizada'
        detalle = f"Tarea '{instance.titulo}' actualizada. Estado: {instance.estado}."
    ProyectoActividad.objects.create(proyecto=proyecto, usuario=usuario, accion=accion, detalle=detalle)

@receiver(post_delete, sender=Tarea)
def tarea_deleted(sender, instance, **kwargs):
    proyecto = instance.proyecto
    ProyectoActividad.objects.create(proyecto=proyecto, usuario=None, accion='Tarea eliminada', detalle=f"Tarea '{instance.titulo}' eliminada.")

@receiver(post_save, sender=Solicitud)
def solicitud_saved(sender, instance, created, **kwargs):
    proyecto = instance.proyecto
    accion = 'Solicitud creada' if created else f"Solicitud actualizada: {instance.estado}"
    detalle = f"Usuario {instance.usuario.username} -> {instance.estado}"
    ProyectoActividad.objects.create(proyecto=proyecto, usuario=instance.usuario, accion=accion, detalle=detalle)

@receiver(post_save, sender=InsigniaOtorgada)
def insignia_otorgada(sender, instance, created, **kwargs):
    if created:
        proyecto = None
        # intentar deducir proyecto por relación del usuario? No siempre disponible
        accion = 'Insignia otorgada'
        detalle = f"Insignia '{instance.insignia.nombre}' otorgada a {instance.usuario.username}"
        # Si la insignia se otorgó dentro del contexto de un proyecto podríamos enlazarla,
        # pero por ahora, guardamos con usuario y sin proyecto (o buscar proyecto por contexto)
        # Para no romper integridad, guardaremos actividad sin proyecto si no hay proyecto
        # pero el modelo requiere proyecto FK — por simplicidad, evitamos crear registro cuando no hay proyecto
        # Si quieres que se registre en un proyecto, pasa 'proyecto' al crear InsigniaOtorgada o ajustamos la lógica.
        # Aquí no creamos registro.
        return

@receiver(m2m_changed, sender=Proyecto.participantes.through)
def participantes_changed(sender, instance, action, pk_set, **kwargs):
    # instance es el proyecto
    if action == 'post_add':
        for uid in pk_set:
            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                user = None
            ProyectoActividad.objects.create(proyecto=instance, usuario=user, accion='Participante agregado', detalle=f"Usuario {user.username} agregado al proyecto.")
    elif action == 'post_remove':
        for uid in pk_set:
            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                user = None
            ProyectoActividad.objects.create(proyecto=instance, usuario=user, accion='Participante removido', detalle=f"Usuario {user.username} removido del proyecto.")
