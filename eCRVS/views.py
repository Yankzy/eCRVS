from .models import Citizen
import json





class CitizenManager:
    def create_citizen(self, **kwargs):
        citizen, created = Citizen.objects.get_or_create(nin=kwargs['nin'])
        if created:
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
    from django.http import HttpResponse
    from .tasks import HeraLifeEventTopicHandler

    data = json.loads(request.body.decode('utf-8'))
    HeraLifeEventTopicHandler(
        nin=data['nin'],
        context=data['context'],
        data=data
    ).handle_event()
    return HttpResponse('OK')

