import graphql_jwt
import graphene
from apps.investments.schema import Query as InvestmentQuery, Mutation as InvestmentMutation
from apps.integrations.schema import Query as ChainQuery, Mutation as ChainMutation


class Query(InvestmentQuery, ChainQuery, graphene.ObjectType):
    pass


class Mutation(InvestmentMutation, ChainMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
