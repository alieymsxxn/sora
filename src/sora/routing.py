from django.urls import path

from sora.consumers import *
from chat.counsumers import *

websocket_urlpatterns = [
    path(route='ws/chatroom/<chatroom_name>', view=ChatroomConsumer.as_asgi()),
]