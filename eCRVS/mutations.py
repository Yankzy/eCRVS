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


class HeraInterface(graphene.Mutation):
    token = graphene.Field(lambda: GenericScalar)

    class Arguments:
        operation = graphene.String(required=True)

    def mutate(self, info, operation):
        if operation:
            raise GraphQLError('Operation string is required')
        try:
            token = HeraAdapter(operation='access_token').get_data()
        except Exception as e:
            token = e
        return HeraInterface(token=token)
    


class CitizenMutations(graphene.ObjectType):
    create_citizen = CreateCitizen.Field()
    delete_citizen = DeleteCitizen.Field()
    hera_access_token = HeraInterface.Field()
