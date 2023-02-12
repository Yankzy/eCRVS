from .models import Citizen
import json
from django.db import IntegrityError





class CitizenManager:
    def create_citizen(self, **kwargs):
        try:
            Citizen.objects.create(nin=kwargs['nin'])
        except IntegrityError:
            import traceback
            traceback.print_exc()
            return None
        
        citizen = Citizen.objects.get(nin=kwargs['nin'])
        citizen.set_password('initial_default_password')
        fields = [field.name for field in Citizen._meta.get_fields()]
        for key, value in kwargs.items():
            if key in fields:
                setattr(citizen, key, value)
        citizen.save()
        return citizen

    def update_citizen(self, **kwargs):
        citizen = Citizen.objects.get(nin=kwargs['nin'])
        fields = [field.name for field in Citizen._meta.get_fields()]
        for key, value in kwargs.items():
            if key in fields:
                setattr(citizen, key, value)
        citizen.save()
        return citizen

    def delete_citizen(self, nin):
        citizen = Citizen.objects.get(nin=nin)
        citizen.delete()
        return citizen


    def get_citizen(self, nin):
        return Citizen.objects.get(nin=nin)


    def change_password(self, nin, password):
        citizen = Citizen.objects.get(nin=nin)
        citizen.set_password(password)
        citizen.save()
        return citizen


def ecrvs_webhook(request):
    "Keep this lightweight and spawn a celery task to handle the event on a separate thread."
    from django.http import HttpResponse
    from .tasks import hera_life_event_handler

    data = json.loads(request.body.decode('utf-8'))
    hera_life_event_handler.delay(data['nin'], data['context'])
    return HttpResponse('OK')

