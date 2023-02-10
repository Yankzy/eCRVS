import graphene
from .types import CitizenType, Input
from .views import CitizenManager
from .adapters import HeraAdapter
from graphene.types.generic import GenericScalar
from graphql.error import GraphQLError
from django.conf import settings
from django.utils import timezone
import logging



manager = CitizenManager()

class CreateCitizen(graphene.Mutation):
    citizen = graphene.Field(lambda: CitizenType)

    class Arguments:
        input = Input(required=True)

    def mutate(self, info, **inputs):
        kwargs = inputs.get('input')
        citizen = manager.create_citizen(**kwargs)
        return CreateCitizen(citizen=citizen)


class DeleteCitizen(graphene.Mutation):
    citizen = graphene.Field(lambda: CitizenType)

    class Arguments:
        input = Input(required=True)

    def mutate(self, info, **inputs):
        kwargs = inputs.get('input')
        citizen = manager.delete_citizen(kwargs['nin'])
        return DeleteCitizen(citizen=citizen)


class HeraAccessToken(graphene.Mutation):
    token = graphene.Field(lambda: GenericScalar)

    class Arguments:
        admin_token = graphene.String(required=True)

    def mutate(self, info, admin_token):
        try:
            if admin_token != 'zVjBVeFdHRkhhRmROTWxKMVYxUkplRll5U25SU2JHeFZZV3RLY1Zsc1ZscGtNV3h':
                raise GraphQLError('Invalid admin token')
            
            hera = HeraAdapter(operation='get_info')
            token = hera.get_data()
        except Exception as e:
            raise GraphQLError('Error fetching access token') from e
        return HeraAccessToken(token=token)
    
    

class CitizenMutations(graphene.ObjectType):
    create_citizen = CreateCitizen.Field()
    delete_citizen = DeleteCitizen.Field()
    hera_access_token = HeraAccessToken.Field()
