from decimal import Decimal

TIER_BRONZE = ("bronze", Decimal("6.0"))
TIER_SILVER = ("silver", Decimal("8.0"))
TIER_GOLD = ("gold", Decimal("10.0"))

def determine_investment_tier(amount: Decimal):
    if amount >= Decimal("50000"):
        return TIER_GOLD
    
    elif amount >= Decimal("10000"):
        return TIER_SILVER
    
    else:
        return TIER_BRONZE