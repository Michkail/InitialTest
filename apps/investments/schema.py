import graphene
from decimal import Decimal
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
        fields = (
            "id", "asset_name", "amount_invested", "purchase_date",
            "current_value", "is_active", "currency"
        )

    def resolve_profit_loss(self, info):
        try:
            return str(Decimal(self.current_value) - Decimal(self.amount_invested))
        except:
            return "0.00"

    def resolve_profit_loss_percentage(self, info):
        try:
            amount = Decimal(self.amount_invested)
            current = Decimal(self.current_value)
            diff = current - amount
            if amount == 0:
                return "0.00"
            return f"{(diff / amount * 100):.2f}"
        except:
            return "0.00"


class YieldPaymentType(DjangoObjectType):
    class Meta:
        model = YieldPayment
        fields = "__all__"


class UserWalletType(DjangoObjectType):
    class Meta:
        model = UserWallet
        fields = "__all__"


class InsightType(graphene.ObjectType):
    average_holding_period_days = graphene.Int()
    average_investment_size = graphene.Float()


class InvestmentSummaryType(graphene.ObjectType):
    total_invested = graphene.String()
    total_value = graphene.String()
    total_profit_loss = graphene.String()
    active_investments = graphene.Int()
    best_performing = graphene.String()
    worst_performing = graphene.String()
    portfolio_roi_percentage = graphene.Float()
    insights = graphene.Field(InsightType)


class InvestmentInput(graphene.InputObjectType):
    asset_name = graphene.String(required=True)
    amount_invested = graphene.String(required=True)
    purchase_date = graphene.DateTime(required=True)
    current_value = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    currency_id = graphene.ID(required=True)
    yield_rate = graphene.String(required=True)


class CreateInvestment(graphene.Mutation):
    class Arguments:
        input = InvestmentInput(required=True)

    investment = graphene.Field(InvestmentType)

    @login_required
    def mutate(self, info, input):
        user = info.context.user
        currency = Currency.objects.get(id=input.currency_id)
        investment = UserInvestment.objects.create(user=user,
                                                   asset_name=input.asset_name,
                                                   amount_invested=Decimal(input.amount_invested),
                                                   current_value=Decimal(input.current_value),
                                                   purchase_date=input.purchase_date,
                                                   is_active=input.is_active,
                                                   currency=currency,
                                                   yield_rate=Decimal(input.yield_rate))
        
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
        
        return InvestmentSummaryType(total_invested=str(data["total_invested"]),
                                     total_value=str(data["total_value"]),
                                     total_profit_loss=str(data["total_profit_loss"]),
                                     active_investments=data["active_investments"],
                                     best_performing=data["best_performing"],
                                     worst_performing=data["worst_performing"],
                                     portfolio_roi_percentage=data["portfolio_roi_percentage"],
                                     insights=InsightType(average_holding_period_days=insights["average_holding_period_days"],
                                                          average_investment_size=insights["average_investment_size"]))


class Mutation(graphene.ObjectType):
    create_investment = CreateInvestment.Field()
