from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from apps.integrations.contracts.settlement import SmartContractSettlementService
from apps.investments.models import UserInvestment, YieldPayment, UserWallet
from apps.investments.constants import determine_investment_tier


class YieldCalculationService:
    def calculate_daily_yields(self):
        now = timezone.now()
        investments = UserInvestment.objects.filter(is_active=True)
        results = []

        for inv in investments:
            last_payment = inv.last_yield_payment or inv.purchase_date
            days_elapsed = (now.date() - last_payment.date()).days

            if days_elapsed < 1:
                continue

            principal = inv.currrent_value
            tier_name, tier_rate = determine_investment_tier(principal)
            daily_rate = tier_rate / Decimal("100.0") / Decimal("365")

            if inv.tier != tier_name:
                inv.tier = tier_name
                inv.save(update_fields=["tier"])

            compound = inv.auto_compound
            total_yield = Decimal("0.0")
            base = principal

            for _ in range(days_elapsed):
                daily_yield = base * daily_rate
                total_yield += daily_yield

                if compound:
                    base += daily_yield

            results.append({
                "investment": inv,
                "amount": total_yield.quantize(Decimal("0.00000001")),
                "days": days_elapsed
            })

        return results

    @transaction.atomic
    def process_yield_distribution(self):
        yield_data = self.calculate_daily_yields()
        now = timezone.now()

        for data in yield_data:
            inv = data['investment']
            amount = data['amount']
            currency = inv.currency
            wallet = UserWallet.objects.select_for_update().get(user=inv.user, currency=currency)

            wallet.balance += amount
            wallet.save()

            svc = SmartContractSettlementService()
            tx_result = svc.send_yield_to_wallet(wallet, amount, currency)
            
            YieldPayment.objects.create(investment=inv,
                                        amount=amount,
                                        currency=currency,
                                        payment_date=now,
                                        transaction_hash=tx_result.get("tx_hash"),
                                        status='completed')

            inv.last_yield_payment = now
            inv.save()