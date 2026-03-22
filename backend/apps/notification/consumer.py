from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return 
        self.group_name =f"user_{user,id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    async def send_notification(self,event):
        await self.send_json({
            "message":event["message"],
            "data":event.get("data",{})
        })
        