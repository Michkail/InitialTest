from .models import UserInvestment
from django.utils import timezone


class InvestmentService:
    def calculate_portfolio_performance(self, user):
        investments = UserInvestment.objects.filter(user=user)
        total_invested = sum(i.amount_invested for i in investments)
        current_total = sum(i.current_value for i in investments)

        if total_invested == 0:
            return 0
        
        return round(((current_total - total_invested) / total_invested) * 100, 2)

    def get_investment_insights(self, user):
        investments = UserInvestment.objects.filter(user=user)

        if not investments.exists():
            return {}

        holding_periods = [(timezone.now() - i.purchase_date).days for i in investments]
        avg_holding = sum(holding_periods) / len(holding_periods)
        avg_size = sum(i.amount_invested for i in investments) / len(investments)

        return {
            "average_holding_period_days": round(avg_holding),
            "average_investment_size": round(avg_size, 2)
        }