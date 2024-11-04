from django.urls import path
from chat.counsumers import ChannelConsumer

websocket_urlpatterns = [
    path(route='chat/ws/channel/<slug:slug>', view=ChannelConsumer.as_asgi()),
]