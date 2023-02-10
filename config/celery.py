
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


app = Celery('config')

app.conf.update(
    enable_utc=True,
    broker_url="redis://localhost:6379",
    result_backend="redis://localhost:6379",
    cache_backend='default',
    result_extended=True,
    accept_content=["application/json"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    task_always_eager=False,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_hijack_root_logger=False
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
