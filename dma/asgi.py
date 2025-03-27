import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dma.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from account.middleware.jwt_auth import JWTAuthMiddleware
from feed.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP Requests handled by Django
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            JWTAuthMiddleware(
                URLRouter(websocket_urlpatterns)
            )
        )
    ),
})
