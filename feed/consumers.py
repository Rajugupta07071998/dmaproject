# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatRoom, Message
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
#         self.room_group_name = f"chat_{self.room_id}"

#         if self.user.is_authenticated:
#             await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         sender = self.user
#         chat_room = await self.get_chat_room(self.room_id)

#         if not chat_room:
#             return

#         message = Message.objects.create(
#             chat_room=chat_room,
#             sender=sender,
#             content=data["message"]
#         )

#         response = {
#             "message_id": str(message.id),
#             "sender": sender.username,
#             "content": message.content,
#             "created_at": str(message.created_at),
#         }

#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": response}
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps(event["message"]))

#     @staticmethod
#     async def get_chat_room(room_id):
#         try:
#             return await ChatRoom.objects.get(id=room_id)
#         except ChatRoom.DoesNotExist:
#             return None






import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        if not text_data or text_data.strip() == "":  # Handle empty message
            await self.send(text_data=json.dumps({"error": "Empty message received"}))
            return

        try:
            data = json.loads(text_data)  # Ensure valid JSON format
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
            return

        sender = self.user
        chat_room = await self.get_chat_room(self.room_id)

        if not chat_room:
            await self.send(text_data=json.dumps({"error": "Chat room not found"}))
            return

        # Convert any non-string values into strings
        message_content = str(data.get("message", ""))

        # Save message in database
        message = await self.create_message(chat_room, sender, message_content)

        response = {
            "message_id": str(message.id),
            "sender": sender.username,
            "content": message.content,
            "created_at": str(message.created_at),
        }

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": response}
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def get_chat_room(self, room_id):
        """Fetch chat room from database in a non-blocking way"""
        try:
            return ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, chat_room, sender, message):
        """Create message in database asynchronously"""
        return Message.objects.create(chat_room=chat_room, sender=sender, content=message)

