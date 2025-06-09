import requests
from decimal import Decimal, ROUND_DOWN


class ExchangeRateService:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"

    def get_rate_to_usd(self, currency_code: str) -> Decimal:
        res = requests.get(self.api_url,
                           params={"ids": currency_code.lower(), "vs_currencies": "usd"},
                           timeout=5)
        
        return Decimal(str(res.json()[currency_code.lower()]["usd"]))

    def convert(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        if from_currency == to_currency:
            return amount

        res = requests.get(self.api_url,
                           params={"ids": f"{from_currency.lower()},{to_currency.lower()}", "vs_currencies": "usd"},
                           timeout=5).json()

        from_usd = Decimal(str(res[from_currency.lower()]["usd"]))
        to_usd = Decimal(str(res[to_currency.lower()]["usd"]))
        converted = (amount * from_usd) / to_usd

        return converted.quantize(Decimal("0.00000001"), rounding=ROUND_DOWN)
