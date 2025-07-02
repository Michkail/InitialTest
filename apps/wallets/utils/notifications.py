from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_transaction_status(user, tx_id, status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"user_{user.id}",
                                            {
                                                "type": "transaction_status_update",
                                                "data": {
                                                    "type": "transaction_status",
                                                     "tx_id": tx_id,
                                                     "status": status
                                                }
                                            })
