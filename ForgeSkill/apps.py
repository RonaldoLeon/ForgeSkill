from django.apps import AppConfig

class ForgeskillConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ForgeSkill'
    def ready(self):
        # Import signals to ensure they are registered
        try:
            import ForgeSkill.signals  # noqa: F401
        except Exception:
            pass