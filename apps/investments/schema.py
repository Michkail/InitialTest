import graphene
from django.utils.timezone import now
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from apps.investments.models import UserInvestment, Currency, UserWallet, YieldPayment
from apps.investments.services.statement_service import InvestmentService

class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency
        fields = ("id", "code", "network", "contract_address", "decimal_places")


class InvestmentType(DjangoObjectType):
    profit_loss = graphene.String()
    profit_loss_percentage = graphene.String()

    class Meta:
        model = UserInvestment
        fields = ("id", "asset_name", "amount_invested", "current_value", "purchase_date", "currency")

    def resolve_profit_loss(self, info):
        return str(self.current_value - self.amount_invested)

    def resolve_profit_loss_percentage(self, info):
        diff = self.current_value - self.amount_invested
        percent = (diff / self.amount_invested) * 100

        if self.amount_invested == 0:
            return "0.00"

        return f"{percent:.2f}"


class YieldPaymentType(DjangoObjectType):
    class Meta:
        model = YieldPayment
        fields = "__all__"


class UserWalletType(DjangoObjectType):
    class Meta:
        model = UserWallet
        fields = "__all__"


class InvestmentSummaryType(graphene.ObjectType):
    total_invested = graphene.String()
    total_value = graphene.String()
    total_profit_loss = graphene.String()
    active_investments = graphene.Int()
    best_performing = graphene.String()
    worst_performing = graphene.String()
    portfolio_roi_percentage = graphene.Float()
    insights = graphene.JSONString()


class CreateInvestment(graphene.Mutation):
    class Arguments:
        input = InvestmentInput(required=True)

    investment = graphene.Field(InvestmentType)

    @login_required
    def mutate(self, info, input):
        user = info.context.user
        currency = Currency.objects.get(id=input.currency_id)
        investment = UserInvestment.objects.create(
            user=user,
            asset_name=input.asset_name,
            amount_invested=input.amount_invested,
            current_value=input.current_value,
            purchase_date=input.purchase_date,
            is_active=input.is_active,
            currency=currency
        )
        return CreateInvestment(investment=investment)
    

class Query(graphene.ObjectType):
    investments = graphene.List(InvestmentType)
    investment = graphene.Field(InvestmentType, id=graphene.Int(required=True))
    yield_payments = graphene.List(YieldPaymentType)
    wallets = graphene.List(UserWalletType)
    currencies = graphene.List(CurrencyType)
    investment_summary = graphene.Field(InvestmentSummaryType)

    @login_required
    def resolve_investments(self, info):
        return UserInvestment.objects.filter(user=info.context.user)

    @login_required
    def resolve_investment(self, info, id):
        return UserInvestment.objects.get(id=id, user=info.context.user)

    @login_required
    def resolve_yield_payments(self, info):
        return YieldPayment.objects.filter(investment__user=info.context.user)

    @login_required
    def resolve_wallets(self, info):
        return UserWallet.objects.filter(user=info.context.user)

    @login_required
    def resolve_currencies(self, info):
        return Currency.objects.all()

    @login_required
    def resolve_investment_summary(self, info):
        service = InvestmentService()
        data = service.calculate_portfolio_performance(info.context.user)
        insights = service.get_investment_insights(info.context.user)
        return InvestmentSummaryType(**data, insights=insights)


class Mutation(graphene.ObjectType):
    create_investment = CreateInvestment.Field()
