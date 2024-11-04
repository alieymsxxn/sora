from django.urls import path
from chat.views import channels, dashboard, private_channels

urlpatterns = [
    # path(route='', view=chat, name='chat'),
    path(route='chat/', view=dashboard, name='dashboard'),
    path(route='chat/channels/<slug:slug>', view=channels, name='channels'),
    path(route='chat/private-channels/<str:client_friend>', view=private_channels, name='private_channels')
]