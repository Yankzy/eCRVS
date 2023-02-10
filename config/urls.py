
from django.urls import path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib import admin
from eCRVS.views import ecrvs_webhook



urlpatterns = [
    path("admin", admin.site.urls),
    path("", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    path("ecrvs-notification/", csrf_exempt(ecrvs_webhook)),
]
