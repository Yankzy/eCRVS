from celery import shared_task


def camel_to_snake(camel_string):
    snake = []
    for i, char in enumerate(camel_string):
        if char.isupper():
            if i != 0:
                snake.append("_")
            snake.append(char.lower())
        else:
            snake.append(char)
    return "".join(snake)


@shared_task(bind=True, max_retries=1)
def hera_life_event_handler(self, nin, context):
    from .adapters import HeraAdapter
    from .views import CitizenManager
    
    try:
        if response := HeraAdapter(nin=nin, operation='get_one_person_info').get_data():
            crud = {
                "CREATE": 'create_citizen',
                "UPDATE": 'update_citizen',
                "DELETE": 'delete_citizen',
            }
            for key, value in crud.items():
                if key in context:
                    citizen_manager_method = getattr(CitizenManager(), value)
                    snake_case_data = {camel_to_snake(key): value for key, value in response.items()}
                    citizen_manager_method(**snake_case_data)
                    break
    except Exception as exc:
        # Schedule a retry of the task in 10 seconds
        raise self.retry(exc=exc, countdown=1) from exc
        
