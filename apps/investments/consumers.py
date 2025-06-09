from channels.generic.websocket import AsyncWebsocketConsumer
from apps.investments.models import UserInvestment


class InvestmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.group_name = f"user_{self.scope['user'].id}"
            
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

        else:
            await self.close()

    async def receive_json(self, content):
        command = content.get("command")

        if command == "portfolio":
            investments = UserInvestment.objects.filter(user=self.scope["user"])
            data = [{
                "asset": inv.asset_name,
                "amount": str(inv.amount_invested),
                "value": str(inv.current_value)
            } for inv in investments]

            await self.send_json({"type": "portfolio_data", "data": data})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
