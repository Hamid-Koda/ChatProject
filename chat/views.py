import time
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message

def get_rule_based_response(user_message):
    user_message = user_message.lower().strip()

    if "سلام" in user_message:
        return "علیک سلام! خوش آمدی."
    elif "چطوری" in user_message or "خوبی" in user_message:
        return "ممنون، من یک ربات هستم و حالم همیشه خوب است! شما چطورید؟"
    elif "ساعت" in user_message:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"ساعت الان {now} است."
    elif "کجا" in user_message:
        return "من روی یک سرور زندگی می‌کنم و همیشه آنلاین هستم!"
    elif "هوا" in user_message:
        return "من به اطلاعات آب و هوای زنده دسترسی ندارم، اما امیدوارم هرجا که هستی هوا عالی باشه! ☀️"
    elif "روز" in user_message or "شب" in user_message:
        hour = datetime.datetime.now().hour
        if 6 <= hour < 18:
            return "الان روزه. وقت کار و تلاشه!"
        else:
            return "الان شبه. وقت استراحت و آرامشه!"
    elif "چخبر" in user_message:
        return "سلامتی! من آماده‌ام تا با شما صحبت کنم. شما چه خبر؟"
    elif "دوستم داری" in user_message:
        return "به عنوان یک هوش مصنوعی، من احساسات ندارم، اما از صحبت کردن با شما بسیار لذت می‌برم! 😊"
    elif "سازندت کیه" in user_message or "کی ساختتت" in user_message:
        return "من توسط یک برنامه‌نویس خلاق ساخته شده‌ام که در حال یادگیری جنگو است."
    elif "چند وقته ساخته شدی" in user_message or "تولد" in user_message:
        return "من یک پروژه در حال توسعه هستم و همین چند روز پیش ساخته شده ام!!!"
    elif "بک اندت چیه" in user_message or "بک‌اند" in user_message:
        return "بک‌اند من با قدرت فریمورک جنگو (Django) و زبان پایتون نوشته شده."
    elif "فرانتت چیه" in user_message or "فرانت‌اند" in user_message:
        return "فرانت‌اند من با HTML و CSS ساده و کمی جاوا اسکریپت برای پویایی ساخته شده." 
    elif "خدا" in user_message or "فعلا" in user_message:
        return "خدانگهدار، روز خوبی رو داشته باشی عزیزم!"   
    else:
        return "متاسفانه متوجه منظورتان نشدم. می‌توانید سوال دیگری بپرسید؟"
    
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

        bot_response_text = get_rule_based_response(user_message_text)
        # ---------------------------

        Message.objects.create(
            conversation=conversation,
            text=bot_response_text,
            is_from_user=False
        )

        return Response({'reply': bot_response_text})


def stream_response_generator(user_message_text):
    bot_response = get_rule_based_response(user_message_text)
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