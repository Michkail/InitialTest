from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_yield_payment(user, amount, currency_code):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"user_{user.id}",
                                            {
                                                "type": "portfolio_update",
                                                "data": {
                                                    "type": "yield_payment",
                                                    "amount": str(amount),
                                                    "currency": currency_code
                                                }
                                            })
    
def notify_price_movement(user, asset, direction, percent):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"user_{user.id}",
                                            {
                                                "type": "portfolio_update",
                                                "data": {
                                                    "type": "price_alert",
                                                    "asset": asset,
                                                    "change": direction,
                                                    "percent": percent
                                                }
                                            })
