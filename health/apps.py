from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .controllers.DataCollector import getCollectBySchedule


class HealthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health'
    def ready(self):
        # from .DataCollector import getCollectBySchedule
        rt=getCollectBySchedule(1)


