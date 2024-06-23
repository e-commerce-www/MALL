from django.apps import AppConfig


class SongsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.songs'

    def ready(self):
        import apps.songs.signals
