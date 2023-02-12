from django.db import models
from uuid import uuid4
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CitizenManager



class Activity(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/
    """Put this model in the app in case you want to track activities of citizens and link them in all interesting ways."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    activity_type = models.CharField(max_length=250, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=250, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.activity_type}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Citizen(AbstractUser):
    
    username = None
    id = models.CharField(primary_key=True, default=uuid4, unique=True, editable=False, max_length=40)
    birth_registration_number = models.CharField(max_length=250, blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    place_of_birth = models.CharField(max_length=250, blank=True, null=True)
    uin = models.CharField(max_length=250, blank=True, null=True)
    nin = models.CharField(max_length=250, blank=True, null=True, unique=True)
    dob = models.CharField(max_length=250, blank=True, null=True)
    certificate_number = models.CharField(max_length=250, blank=True, null=True)
    activities = GenericRelation(Activity, related_query_name='activities')

    objects = CitizenManager()

    USERNAME_FIELD = "nin"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nin
