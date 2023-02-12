import graphene
from .types import CitizenType, Input
from .views import CitizenManager
from .adapters import HeraAdapter
from graphene.types.generic import GenericScalar
from graphql.error import GraphQLError



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
        # if admin_token != 'JHeFZZV3RLY1Zsc1ZscGtNV3h':
        #     raise GraphQLError('Invalid admin token')
        try:
            hera = HeraAdapter(operation='access_token')
            token = hera.get_data()
            print(admin_token)
        except Exception as e:
            raise GraphQLError('Error fetching access token') from e
        return HeraAccessToken(token=token)
    


class CitizenMutations(graphene.ObjectType):
    create_citizen = CreateCitizen.Field()
    delete_citizen = DeleteCitizen.Field()
    hera_access_token = HeraAccessToken.Field()
