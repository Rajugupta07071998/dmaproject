from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>[a-f0-9\-]+)/$", ChatConsumer.as_asgi()),
]

# from django.urls import path
# from feed.consumers import ChatConsumer

# websocket_urlpatterns = [
#     path("ws/chat/<uuid:chat_room_id>/", ChatConsumer.as_asgi()), 
# ]
