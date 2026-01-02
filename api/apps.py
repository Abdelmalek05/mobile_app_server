from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        try:
            import api.signals
        except Exception as e:
            print(f"Warning: Failed to import signals: {str(e)}")
