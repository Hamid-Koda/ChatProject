from django.urls import path
from .views import chat_page, ChatAPIView, ChatStreamAPIView 
urlpatterns = [
    path('chat/', chat_page, name='chat_page'),
    path('api/chat/', ChatAPIView.as_view(), name='chat_api'),
    path('api/chat/stream/', ChatStreamAPIView.as_view(), name='chat_api_stream'),
]
