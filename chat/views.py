from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message

def home(request):
    return render(request, 'home.html')

@login_required
def chat_page(request):
    """صفحه‌ای که چت در آن نمایش داده می‌شود"""
    return render(request, 'chat.html')


class ChatAPIView(APIView):
    """API برای چت با روش HTTP"""
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
