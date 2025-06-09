import graphene
from graphene_django.types import DjangoObjectType
from apps.investments.models import UserInvestment
from apps.analytics.services.summary_reader import get_user_investment_summary
from django.contrib.auth import get_user_model


class InvestmentType(DjangoObjectType):
    class Meta:
        model = UserInvestment
        fields = ("id", "asset_name", "amount_invested", "current_value", "purchase_date", "currency")


class InvestmentSummaryType(graphene.ObjectType):
    total_invested = graphene.Decimal()
    total_value = graphene.Decimal()
    investment_count = graphene.Int()


class Query(graphene.ObjectType):
    investments = graphene.List(InvestmentType)
    investment_summary = graphene.Field(InvestmentSummaryType)

    def resolve_investments(self, info):
        user = info.context.user
        return UserInvestment.objects.filter(user=user)

    def resolve_investment_summary(self, info):
        user = info.context.user
        row = get_user_investment_summary(user.id)

        if not row:
            return InvestmentSummaryType(total_invested=0, total_value=0, investment_count=0)
        
        return InvestmentSummaryType(investment_count=row[1],
                                     total_invested=row[2],
                                     total_value=row[3])
