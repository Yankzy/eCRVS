from celery import shared_task
from .adapters import HeraAdapter
from dataclasses import dataclass
from typing import Dict, Any
from celery.result import AsyncResult


@shared_task(bind=True, max_retries=5)
def get_from_api(self, **kwargs):
    try:
        adapter = globals().get(kwargs.pop('adapter'))
        return adapter(**kwargs).get_data()
    except Exception as exc: 
        # Schedule a retry of the task in 10 seconds
        raise self.retry(exc=exc, countdown=10) from exc


@dataclass
class HeraLifeEventTopicHandler:
    from .views import CitizenManager
    nin: str
    context: str
    data: Dict[str, str] = None
    

    def handle_event(self):
        crud = {
            "CREATE": self.handle_create,
            "UPDATE": self.handle_update,
            "DELETE": self.handle_delete,
        }
        for key, value in crud.items():
            if key in self.context:
                value()
                break

    def handle_create(self):
        result = get_from_api.apply_async(
            kwargs={
                'adapter': 'HeraAdapter',
                'nin': self.nin,
                'operation': 'get_one_person_info',
                'callback': 'create_citizen'
            },
            task_id='handle_create'
        )
        async_result = AsyncResult(result.id)
        if async_result.successful():
            print(async_result.get())

    def handle_update(self):
        result = get_from_api.apply_async(
            kwargs={
                'adapter': 'HeraAdapter',
                'nin': self.nin,
                'operation': 'get_one_person_info',
            },
            task_id='handle_update'
        )
        async_result = AsyncResult(result.id)
        if async_result.successful():
            print(async_result.get())

    def handle_delete(self):
        result = get_from_api.apply_async(
            kwargs={
                'adapter': 'HeraAdapter',
                'nin': self.nin,
                'operation': 'get_one_person_info',
            },
            task_id='handle_delete'
        )
        async_result = AsyncResult(result.id)
        if async_result.successful():
            print(async_result.get())
