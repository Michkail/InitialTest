from decimal import Decimal
from apps.integrations.exchange.providers import ExchangeRateService


def convert_currency(amount: Decimal, from_code: str, to_code: str) -> Decimal:
    return ExchangeRateService().convert(amount, from_code, to_code)
