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
    """
    Hera Interface Mutation.
    These are the valid operations:
        * access_token,
        * get_one_person_info,
        * get__bulk_info,
        * verify,
        * match,
        * document,
        * get_subscriptions,
        * subscribe_to_life_event,
        * confirm_subscription,
        * unsubscribe_from_topic,
        * create_topic,
        * get_topics,
        * delete_topic,
        * publish_topic,
    
        Calling any of these operations, you need to pass the operation name as an argument and nin (except for access_token).
    """
    token = graphene.Field(lambda: GenericScalar)

    class Arguments:
        operation = graphene.String(required=True)
        nin = graphene.String()

    def mutate(self, info, operation, nin=None):
        if not operation:
            raise GraphQLError('Operation string is required')
        try:
            token = HeraAdapter(operation=operation, nin=nin).get_data()
        except Exception as e:
            token = e
        return HeraInterface(token=token)
    


class CitizenMutations(graphene.ObjectType):
    create_citizen = CreateCitizen.Field()
    delete_citizen = DeleteCitizen.Field()
    hera_interface = HeraInterface.Field()
