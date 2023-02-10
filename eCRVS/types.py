import graphene
from .models import Citizen
from graphene_django import DjangoObjectType


class CitizenType(DjangoObjectType):
    class Meta:
        model = Citizen
        exclude_fields = ['password']


class Input(graphene.InputObjectType):
    birth_registration_number = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    place_of_birth = graphene.String()
    uin = graphene.String()
    nin = graphene.String()
    password = graphene.String()