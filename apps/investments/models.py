from django.db import models
from django.contrib.auth.models import User


class UserInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_name = models.CharField()
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField()


class TransactionChoices(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"
    PURCHASE = "purchase", "Purchase"


class TransactionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TransactionChoices.choices, default=TransactionChoices.DEPOSIT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField()
    reference_id = models.CharField(unique=True)
