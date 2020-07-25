from django.apps import AppConfig


class BookmarkerConfig(AppConfig):
    name = 'bookmarker'

    def ready(self):
        import bookmarker.signals
