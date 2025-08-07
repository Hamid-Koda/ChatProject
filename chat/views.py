import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message

def home(request):
    return render(request, 'home.html')

@login_required
def chat_page(request):
    """Renders the page where the chat interface is displayed."""
    return render(request, 'chat.html')

class ChatAPIView(APIView):
    """API for handling a standard, non-streaming chat request."""
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        user_message_text = request.data.get('message')
        if not user_message_text:
            return Response({'error': 'Message not provided'}, status=400)

        conversation, created = Conversation.objects.get_or_create(user=request.user)

        Message.objects.create(
            conversation=conversation,
            text=user_message_text,
            is_from_user=True
        )

        bot_response_text = f"علیک السلام! پیام شما '{user_message_text}' دریافت شد."
        # ---------------------------

        Message.objects.create(
            conversation=conversation,
            text=bot_response_text,
            is_from_user=False
        )

        return Response({'reply': bot_response_text})


def stream_response_generator(user_message_text):
    """
    This is a generator function. It uses 'yield' instead of 'return' 
    to send the response in multiple parts.
    """
    bot_response = f"این یک پاسخ استریم شده به پیام شما '{user_message_text}' است."
    for word in bot_response.split():
        yield word + " "
        time.sleep(0.1) 

class ChatStreamAPIView(APIView):
    """API for handling a streaming chat request."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message_text = request.data.get('message')
        if not user_message_text:
            return Response({'error': 'Message not provided'}, status=400)

        conversation, created = Conversation.objects.get_or_create(user=request.user)
        Message.objects.create(
            conversation=conversation,
            text=user_message_text,
            is_from_user=True
        )

        return StreamingHttpResponse(stream_response_generator(user_message_text))