import graphene
from graphene_django.debug import DjangoDebug
from eCRVS.mutations import CitizenMutations




class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(CitizenMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
