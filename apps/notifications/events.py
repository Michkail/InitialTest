from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def emit_event(user_id, event_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"user_{user_id}",
                                            {
                                                "type": "portfolio_update",
                                                "data": {
                                                    "type": event_type,
                                                    **data
                                                }
                                            })
