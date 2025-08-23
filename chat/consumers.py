import json
import time
from channels.generic.websocket import WebsocketConsumer
from .models import Conversation, Message
from .views import get_rule_based_response

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #self.user = self.scope["user"]
        #if not self.user.is_authenticated:
            #self.close()
        #else:
            #self.accept()
        # برای تست با پست‌من، به همه اجازه اتصال می‌دهیم
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        user = self.scope["user"] 
        text_data_json = json.loads(text_data)
        user_message_text = text_data_json['message']

        # پاسخ ربات را آماده می‌کنیم
        bot_response_text = get_rule_based_response(user_message_text)

        # فقط اگر کاربر لاگین کرده بود، گفتگو را ذخیره می‌کنیم
        if user.is_authenticated:
            conversation, _ = Conversation.objects.get_or_create(user=user)
            Message.objects.create(conversation=conversation, text=user_message_text, is_from_user=True)
            Message.objects.create(conversation=conversation, text=bot_response_text, is_from_user=False)
        
        self.send(text_data=json.dumps({
            'reply': bot_response_text
        }, ensure_ascii=False))


class StreamChatConsumer(WebsocketConsumer):
    def connect(self):
        #self.user = self.scope["user"]
        #if not self.user.is_authenticated:
            #self.close()
        #else:
            #self.accept()
        # برای تست با پست‌من، به همه اجازه اتصال می‌دهیم
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        user = self.scope["user"] 
        text_data_json = json.loads(text_data)
        user_message_text = text_data_json['message']

        # فقط اگر کاربر لاگین کرده بود، پیام او را ذخیره می‌کنیم
        if user.is_authenticated:
            conversation, _ = Conversation.objects.get_or_create(user=user)
            Message.objects.create(conversation=conversation, text=user_message_text, is_from_user=True)
        
        # پاسخ ربات را آماده و به صورت استریم ارسال می‌کنیم
        bot_response_text = get_rule_based_response(user_message_text)
        for word in bot_response_text.split():
            self.send(text_data=json.dumps({'chunk': word + '\u00A0'}, ensure_ascii=False))
            time.sleep(0.1)


#connect to web socket in postman : ws://127.0.0.1:8000/ws/chat/stream/

#connect to swagger : http://127.0.0.1:8000/api/schema/swagger-ui/

#connect to daphne server : daphne -p 8000 core.asgi:application