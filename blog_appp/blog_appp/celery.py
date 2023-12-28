from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog_appp.settings')

app = Celery('blog_appp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat 
app.conf.beat_schedule = {
    'send-new-blog-notifications': {
        'task': 'blogs.task.notify',
        'schedule': crontab(minute='*/2'),  # Schedule to run every 2 minutes
                                            # It will sent mail to users like any blog published within before 5 minutes
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
