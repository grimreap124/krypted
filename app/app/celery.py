import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

from django.conf import settings

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_default_queue = settings.CELERY_QUEUE
app.conf.task_routes = settings.CELERY_ROUTES

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(
        lambda: settings.INSTALLED_APPS + settings.INSTALLED_APPS_WITH_CONFIGS
        )
