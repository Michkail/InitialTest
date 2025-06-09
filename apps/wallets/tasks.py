from celery import shared_task
from apps.wallets.services.exchange_service import update_currency_rates_from_sources


@shared_task
def update_currency_rates():
    update_currency_rates_from_sources()
