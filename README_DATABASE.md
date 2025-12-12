# ForgeSkill - Documentación de Base de Datos

## 📋 Información General

**Base de datos:** MySQL  
**Motor:** InnoDB  
**Charset:** utf8mb4  
**Collation:** utf8mb4_unicode_ci  
**Versión Django:** 6.0

---

## 📦 Archivos de Base de Datos

### `forgeskill_database_schema.sql`
Esquema SQL completo de la base de datos generado automáticamente desde las migraciones de Django.

**Uso:**
```bash
# Importar el esquema en MySQL
mysql -u root -p < forgeskill_database_schema.sql
```

**Contiene:**
- Creación de base de datos
- Todas las tablas del proyecto
- Relaciones (Foreign Keys)
- Índices y constraints
- Campos con tipos de datos correctos

---

## 🗄️ Estructura de Tablas

### Tablas Principales:

1. **ForgeSkill_proyecto** - Proyectos del sistema
   - Campos: nombre, descripcion, dificultad, imagen, estado, limite_miembros, progreso
   - Relaciones: lider (User), participantes (Many-to-Many)

2. **ForgeSkill_tarea** - Actividades de proyectos
   - Campos: titulo, descripcion, estado, fecha_entrega, fecha_asignacion, fecha_completado
   - Archivos: archivo_evidencia
   - Estados: pendiente, en_progreso, completada

3. **ForgeSkill_perfil** - Perfiles de usuario
   - Campos: foto, bio, area_trabajo, telefono, ciudad, nivel_estudio, idiomas, conocimientos
   - Relación: user (OneToOne)

4. **ForgeSkill_insignia** - Sistema de gamificación
   - Campos: nombre, descripcion, puntos, imagen
   - Relación con InsigniaOtorgada

5. **ForgeSkill_solicitud** - Postulaciones a proyectos
   - Estados: pendiente, aprobada, rechazada

6. **ForgeSkill_mensaje** - Sistema de mensajería
   - Relaciones: remitente, receptor

7. **ForgeSkill_examen** - Sistema de evaluación
   - Preguntas (opción múltiple, verdadero/falso)
   - Resultados

---

## 🔄 Migraciones Aplicadas

- **0001**: Modelos iniciales
- **0002**: Descripción y dificultad en proyectos
- **0003**: Participantes en proyectos
- **0004**: Imágenes en proyectos
- **0005**: Idiomas y nivel de estudio en perfil
- **0006**: Límite de miembros y progreso
- **0007**: Sistema de insignias completo
- **0008**: Actividades de proyecto
- **0009**: Habilidades y lenguajes en proyectos, conocimientos en perfil
- **0010**: Sistema de fechas y retrasos en tareas

---

## ⚙️ Configuración de Base de Datos

### En `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forgeskill',
        'USER': 'root',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 🚀 Instalación desde Cero

1. **Instalar MySQL**
   ```bash
   # Windows: Descargar MySQL Installer
   # Linux: sudo apt install mysql-server
   ```

2. **Crear base de datos**
   ```sql
   CREATE DATABASE forgeskill CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Importar esquema**
   ```bash
   mysql -u root -p forgeskill < forgeskill_database_schema.sql
   ```

4. **Ejecutar migraciones Django (opcional)**
   ```bash
   python manage.py migrate
   ```

---

## 📝 Notas Importantes

- El archivo SQL es **independiente** del proyecto Django
- Puede usarse para recrear la estructura en cualquier servidor MySQL
- No incluye datos de prueba, solo la estructura
- Las tablas de Django (`auth_user`, `django_migrations`, etc.) se crean automáticamente al ejecutar `migrate`

---

## 🔐 Seguridad

**⚠️ IMPORTANTE:**
- Cambiar la contraseña en `settings.py` en producción
- No exponer credenciales en repositorios públicos
- Usar variables de entorno para información sensible

---

## 📊 Estadísticas del Esquema

- **Total de tablas:** 15+ (incluyendo tablas de Django)
- **Relaciones:** Many-to-Many, ForeignKey, OneToOne
- **Campos de archivo:** ImageField, FileField
- **Tipos de datos:** VARCHAR, LONGTEXT, INTEGER, BIGINT, DATE, DATETIME, DOUBLE

---

Generado: 2025-12-12
