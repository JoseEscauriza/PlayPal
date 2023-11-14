import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message
from apps.user.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomId = self.scope['url_route']['kwargs']['roomId']
        self.room_group_name = f'chat_{self.roomId}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message_content']
        senderId = data['senderId']
        receiverId = data['receiverId']
        roomId = data['roomId']

        await self.save_message(senderId, receiverId, roomId, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_content': message_content,
                'senderId': senderId,
            }
        )


    async def chat_message(self, event):
        message_content = event['message_content']
        if message_content == "":
            pass
        else:
            senderId = event['senderId']
            await self.send(text_data=json.dumps({
                'message_content': message_content,
                'senderId': senderId,
            }))


    @sync_to_async
    def save_message(self, senderId, receiverId, roomId, message_content):
        sender = CustomUser.objects.get(uuid=senderId)
        receiver = CustomUser.objects.get(uuid=receiverId)
        room = Room.objects.get(uuid=roomId)
        
        if message_content != "":
            Message.objects.create(
                sender=sender, 
                recipient=receiver, 
                room=room, 
                content=message_content, 
                is_read=False
                )
