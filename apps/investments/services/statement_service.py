import io
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.investments.models import UserInvestment


class StatementService:
    def generate_pdf(self, user):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Investment Summary for {user.username}")
        p.drawString(100, 780, f"Total Investments: {user.investments.count()}")
        p.showPage()
        p.save()
        buffer.seek(0)

        return buffer

    def send_email(self, user, pdf_buffer):
        email = EmailMessage(
            subject="Your Investment Statement",
            body="Attached is your latest portfolio summary.",
            to=[user.email]
        )
        email.attach("statement.pdf", pdf_buffer.read(), "application/pdf")
        email.send()

    def generate_and_send_all(self):
        User = get_user_model()

        for user in User.objects.all():
            pdf = self.generate_pdf(user)
            self.send_email(user, pdf)


class InvestmentService:
    def calculate_portfolio_performance(self, user):
        investments = UserInvestment.objects.filter(user=user)

        if not investments.exists():
            raise ValueError("User has no investments")

        total_invested = sum(i.amount_invested for i in investments)
        total_value = sum(i.current_value for i in investments)
        total_profit_loss = total_value - total_invested
        portfolio_roi_percentage = 0.0

        if total_invested > 0:
            portfolio_roi_percentage = round(((total_value - total_invested) / total_invested) * 100, 2)

        best = max(investments, key=lambda x: x.current_value - x.amount_invested)
        worst = min(investments, key=lambda x: x.current_value - x.amount_invested)

        return {
            "total_invested": total_invested,
            "total_value": total_value,
            "total_profit_loss": total_profit_loss,
            "active_investments": investments.filter(is_active=True).count(),
            "best_performing": best.asset_name,
            "worst_performing": worst.asset_name,
            "portfolio_roi_percentage": portfolio_roi_percentage,
        }



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