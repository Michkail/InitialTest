from celery import shared_task
from apps.wallets.services.exchange_service import convert_currency


@shared_task
def update_currency_rates():
    convert_currency()
