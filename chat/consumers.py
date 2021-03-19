import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = ''
        self.room_name = ''

    async def connect(self):
        self.room_group_name = 'chat_%s' % self.room_name
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Join room group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket.
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Save message to database.
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group.
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Save message to database.
        # await self.save_message(message)

        # Send message to WebSocket.
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Create message object in database.
    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(
            room=Room.objects.get(name=self.room_name),  # Room object.
            user=self.scope['user'],  # User object.
            text=message,  # Message text content.
        )
