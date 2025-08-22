import os
from django.core.asgi import get_asgi_application

# مرحله ۱: اول از همه، به جنگو می‌گوییم تنظیماتش کجاست
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# مرحله ۲: این خط جنگو را به طور کامل راه‌اندازی و آماده به کار می‌کند
django_asgi_app = get_asgi_application()

# مرحله ۳: حالا که جنگو آماده است، می‌توانیم ماژول‌های دیگر را وارد کنیم
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({ 
    "http": django_asgi_app, 
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})