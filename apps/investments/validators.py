from rest_framework.exceptions import ValidationError


def validate_transaction_data(data):
    if data["amount"] <= 0:
        raise ValidationError("Amount must be positive.")
