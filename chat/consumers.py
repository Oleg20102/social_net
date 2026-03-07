import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from channels.db import database_sync_to_async

from accounts.models import OnlineStatus  # ✅ додаємо

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope["url_route"]["kwargs"]["username"]
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # ✅ ONLINE тут
        await self.set_online(self.user)

        users = sorted([self.user.username, self.other_username])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # ✅ OFFLINE тут
        if getattr(self, "user", None) and self.user.is_authenticated:
            await self.set_offline(self.user)

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get("text")

        if not text:
            return

        other_user = await self.get_other_user()
        await self.save_message(other_user, text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": self.user.username,
                "text": text
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "text": event["text"]
        }))

    @database_sync_to_async
    def get_other_user(self):
        return User.objects.get(username=self.other_username)

    @database_sync_to_async
    def save_message(self, receiver, text):
        Message.objects.create(
            sender=self.user,
            receiver=receiver,
            text=text
        )

    # ✅ ОЦЕ ДОДАТИ В КІНЕЦЬ ФАЙЛУ
    @database_sync_to_async
    def set_online(self, user):
        obj, _ = OnlineStatus.objects.get_or_create(user=user)
        obj.is_online = True
        obj.save()

    @database_sync_to_async
    def set_offline(self, user):
        obj, _ = OnlineStatus.objects.get_or_create(user=user)
        obj.is_online = False
        obj.save()
