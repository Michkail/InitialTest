from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/investments/", consumers.InvestmentConsumer.as_asgi())
]