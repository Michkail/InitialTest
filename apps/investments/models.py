from django.db import models
from django.conf import settings


class Currency(models.Model):
    code = models.CharField(max_length=10)
    network = models.CharField(max_length=20)
    contract_address = models.CharField(max_length=255)
    decimal_places = models.IntegerField()

    def _str_(self):
        return f"{self.code} ({self.network})"
    

class UserInvestment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset_name = models.CharField()
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateTimeField()
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    yield_rate = models.DecimalField(max_digits=5, decimal_places=2)
    last_yield_payment = models.DateTimeField(null=True, blank=True)
    auto_compound = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['user', 'purchase_date']),
                   models.Index(fields=['currency'])]


class TransactionChoices(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"
    PURCHASE = "purchase", "Purchase"


class TransactionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TransactionChoices.choices, default=TransactionChoices.DEPOSIT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField()
    reference_id = models.CharField(unique=True)
    

class UserWallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    locked_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    class Meta:
        unique_together = ('user', 'currency')

    def _str_(self):
        return f"{self.user.username} - {self.currency.code}"


class YieldPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    investment = models.ForeignKey(UserInvestment, on_delete=models.CASCADE, related_name='yield_payments')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    payment_date = models.DateTimeField()
    transaction_hash = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
