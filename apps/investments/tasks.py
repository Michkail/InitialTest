from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from apps.investments.services import InvestmentService
from apps.investments.services.statement_service import StatementService
from apps.investments.services.yield_calculation_service import YieldCalculationService
from apps.investments.utils.notifications import notify_yield_payment


def send_portfolio_value_updates():
    channel_layer = get_channel_layer()
    service = InvestmentService()

    for user in User.objects.all():
        value = service.calculate_portfolio_value(user)
        async_to_sync(channel_layer.group_send)(f"user_{user.id}",
                                                {
                                                    "type": "portfolio_update",
                                                    "data": {
                                                        "type": "portfolio_value",
                                                        "value": str(value),
                                                        "currency": "USDT"
                                                    }
                                                })

@shared_task
def process_yield_payments():
    service = YieldCalculationService()
    results = service.process_yield_distribution(batch=True, batch_size=1000)

    for result in results:
        notify_yield_payment(result['user'],
                             result['amount'],
                             result['currency'])

@shared_task
def generate_monthly_statements():
    StatementService().generate_and_send_all()

