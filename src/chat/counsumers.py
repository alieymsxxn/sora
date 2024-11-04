import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from chat.models import Channel, Message


class ChannelConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.slug = self.scope['url_route']['kwargs']['slug'] 
        self.channel = get_object_or_404(Channel, slug=self.slug)
        async_to_sync(self.channel_layer.group_add)(self.slug, self.channel_name)
        # # Increase online users count
        self.channel.online_users.add(self.user)
        # # Broadcast online users count to all users active
        # online_count = self.chatroom.online_users.count() - 1
        # event = {
        #     'type': 'online_notifier',
        #     'online_count': online_count
        # }
        # async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
        return super().connect()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.slug, self.channel_name)
        # Decrease online users count
        self.channel.online_users.remove(self.user)
        # Broadcast online users count to all users active
        # online_count = self.chatroom.online_users.count() - 1
        # event = {
        #     'type': 'online_notifier',
        #     'online_count': online_count
        # }
        # async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
        return super().disconnect(code)
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = Message.objects.create(
            sender=self.user,
            channel=self.channel,
            body = body,
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id
        }
        async_to_sync(self.channel_layer.group_send)(self.slug, event)
        # context = {
        #     "messages": [message],
        #     "user": self.user
        # }
        # html = render_to_string(template_name='chat/partials/bubbles.html', context=context)
        # self.send(text_data=html)

    def message_handler(self, event):
        message_id = event['message_id']
        messages = Message.objects.filter(id=message_id)
        context = {
            "messages": messages,
            "user": self.user,
            "is_counsumer": True
        }
        html = render_to_string(template_name='chat/dashboard/partials/message_box/messages_list.html', context=context)
        print(html)
        self.send(text_data=html)

    # def online_notifier(self, event):
    #     online_count = event['online_count']
    #     context = {
    #         'online_count': online_count
    #     }
    #     html = render_to_string(template_name='chat/partials/online_count.html', context=context)
    #     self.send(text_data=html)

