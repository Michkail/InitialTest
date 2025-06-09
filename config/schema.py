import graphql_jwt
import graphene
from apps.investments.schema import Query as InvestmentQuery, Mutation as InvestmentMutation


class Query(InvestmentQuery, graphene.ObjectType):
    pass


class Mutation(InvestmentMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
