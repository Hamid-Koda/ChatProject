from django.urls import path
from .views import chat_page, ChatAPIView

urlpatterns = [
    path('chat/', chat_page, name='chat_page'),
    path('api/chat/', ChatAPIView.as_view(), name='chat_api'),
]