from django.contrib import admin
from django.urls import path
from ForgeSkill.views import dashboard_view, proyectos_list, proyecto_detalle,mis_proyectos, perfil, chat, notificaciones, chats_list
from ForgeSkill.views import crear_proyecto, block_user, change_role
from ForgeSkill.views import approve_project, reject_project
from ForgeSkill.views import join_project, leave_project
from ForgeSkill.views import  login_view, home_view, resitro_view, recuperacion_view , usuario_view, logout_view
from ForgeSkill.views import agregar_experiencia, generar_pdf
from ForgeSkill.views import gestion_proyecto, otorgar_insignia, admin_dashboard
from ForgeSkill.views import crear_tarea, editar_tarea, eliminar_tarea, lista_examenes, crear_pregunta
from ForgeSkill.views import tomar_examen
from ForgeSkill.views import lista_insignias, otorgar_insignia_mentor
from ForgeSkill.views import foro_proyecto, postular, cancel_postulacion, approve_solicitud, reject_solicitud
from .views import login_view, root_redirect,admin_panel
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # -- RUTAS ADMIN PERSONALIZADAS (registrarlas ANTES de admin.site.urls)
    path('admin/block_user/<int:user_id>/', block_user, name='block_user'),
    path('admin/change_role/<int:user_id>/', change_role, name='change_role'),
    path('admin/proyecto/aprobar/<int:proyecto_id>/', approve_project, name='approve_project'),
    path('admin/proyecto/rechazar/<int:proyecto_id>/', reject_project, name='reject_project'),
    path('admin/insignias/', lista_insignias, name='lista_insignias'),

    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('', root_redirect, name='root'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('registro/', resitro_view, name='registro'),
    path('recuperacion/', recuperacion_view, name='recuperacion'),
    path('logout/', logout_view, name='logout'),
    path('usuario/', usuario_view, name='usuario'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('proyectos_list/', proyectos_list, name='proyectos_list'),
    path('proyecto_detalle/<int:proyecto_id>/', proyecto_detalle, name='proyecto_detalle'),
    path('mis_proyectos.html/', mis_proyectos, name= 'mis_proyectos'),
    path("perfil/", perfil, name="perfil"),
    path("perfil/experiencia/agregar/", agregar_experiencia, name="agregar_experiencia"),
    path("perfil/pdf/", generar_pdf, name="generar_pdf"),
    path('notificaciones/', notificaciones, name='notificaciones'),
    path('chat/<int:user_id>/', chat, name='chat'), 
    path('chats/', chats_list, name='chats_list'),
    path('proyecto/crear/', crear_proyecto, name='crear_proyecto'),
    path('proyecto/unirse/<int:proyecto_id>/', join_project, name='join_project'),
    path('proyecto/abandonar/<int:proyecto_id>/', leave_project, name='leave_project'),
    path('mentor/proyecto/<int:proyecto_id>/', gestion_proyecto, name='gestion_proyecto'),
    path('mentor/solicitud/aprobar/<int:solicitud_id>/', approve_solicitud, name='approve_solicitud'),
    path('mentor/solicitud/rechazar/<int:solicitud_id>/', reject_solicitud, name='reject_solicitud'),
    path('mentor/insignias/', otorgar_insignia, name='otorgar_insignia'),
    # admin_panel ya está mapeado a la vista personalizada `admin_panel` arriba
    path('mentor/tarea/crear/<int:proyecto_id>/', crear_tarea, name='crear_tarea'),
    path('mentor/tarea/editar/<int:tarea_id>/', editar_tarea, name='editar_tarea'),
    path('mentor/tarea/eliminar/<int:tarea_id>/', eliminar_tarea, name='eliminar_tarea'),
    path('proyecto/<int:proyecto_id>/examenes/', lista_examenes, name='lista_examenes'),
    path('examen/<int:examen_id>/pregunta/nueva/', crear_pregunta, name='crear_pregunta'),
    path('examen/<int:examen_id>/tomar/', tomar_examen, name='tomar_examen'),
    # la ruta 'admin/insignias/' ya está registrada arriba
    path('mentor/otorgar-insignia/', otorgar_insignia_mentor, name='otorgar_insignia_mentor'),
    path('proyecto/<int:proyecto_id>/foro/', foro_proyecto, name='foro_proyecto'),
    path('postular/<int:proyecto_id>/', postular, name='postular'),
    path('postular/cancelar/<int:proyecto_id>/', cancel_postulacion, name='cancel_postulacion'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
