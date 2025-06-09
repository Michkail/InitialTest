from apps.integrations.exchange.providers import ExchangeRateService


def get_rate(from_currency, to_currency):
    provider = ExchangeRateService()
    
    return provider.convert(from_currency, to_currency)
