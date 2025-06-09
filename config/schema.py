import graphene
import apps.investments.schema as investments_schema


class Query(investments_schema.Query,
            graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
