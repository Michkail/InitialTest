from apps.investments.ml.fraud_detector import FraudDetector
from decimal import Decimal
import logging

logger = logging.getLogger("audit")

class MultiCurrencyTransactionEngine:
    def __init__(self, user):
        self.user = user

    def convert_currency(self, amount: Decimal, from_currency, to_currency) -> Decimal:
        dummy_rate = Decimal("1.05")
        
        return amount * dummy_rate

    def calculate_fee(self, currency: 'Currency') -> Decimal:
        network_fees = {
            "ERC20": Decimal("5.00"),
            "TRC20": Decimal("1.00"),
            "BEP20": Decimal("0.50"),
        }

        return network_fees.get(currency.network, Decimal("2.00"))

    def validate_min_transaction(self, currency: 'Currency', amount: Decimal):
        min_amounts = {
            "USDT": Decimal("10.00"),
            "ETH": Decimal("0.01"),
        }

        min_required = min_amounts.get(currency.code, Decimal("1.00"))

        if amount < min_required:
            raise ValueError(f"Minimum amount for {currency.code} is {min_required}")

    def perform_atomic_swap(self, from_wallet, to_wallet, amount: Decimal):
        detector = FraudDetector()
        if detector.predict(amount, from_wallet.currency, "purchase"):
            logger.warning(f"[FRAUD DETECTED] user={from_wallet.user.id} currency={from_wallet.currency.code} amount={amount}")
            raise Exception("Suspicious transaction blocked by fraud detector.")

        from_wallet.balance -= amount
        from_wallet.save()

        to_wallet.balance += amount
        to_wallet.save()

        return True