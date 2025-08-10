import json
import time
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Conversation, Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
        else:
            self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message_text = text_data_json['message']

        conversation, _ = Conversation.objects.get_or_create(user=self.user)
        Message.objects.create(
            conversation=conversation, text=user_message_text, is_from_user=True
        )

        bot_response_text = f"پاسخ وب‌سوکت: '{user_message_text}' دریافت شد."
        Message.objects.create(
            conversation=conversation, text=bot_response_text, is_from_user=False
        )

        self.send(text_data=json.dumps({
            'reply': bot_response_text
        }))


class StreamChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
        else:
            self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_message_text = text_data_json['message']
        conversation, _ = Conversation.objects.get_or_create(user=self.user)
        Message.objects.create(
            conversation=conversation, text=user_message_text, is_from_user=True
        )

        bot_response_text = f"پاسخ استریم شده وب‌سوکت: '{user_message_text}' دریافت شد."
        
        for word in bot_response_text.split():
            self.send(text_data=json.dumps({'chunk': word + '\u00A0'}))
            time.sleep(0.1) 