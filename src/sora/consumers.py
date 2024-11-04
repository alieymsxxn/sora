import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    pass
    # def connect(self):
    #     self.user = self.scope['user']
    #     self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] 
    #     self.chatroom = get_object_or_404(ChatGroup, name='Public Chat')
    #     async_to_sync(self.channel_layer.group_add)(self.chatroom_name, self.channel_name)
    #     # Increase online users count
    #     self.chatroom.online_users.add(self.user)
    #     # Broadcast online users count to all users active
    #     online_count = self.chatroom.online_users.count() - 1
    #     event = {
    #         'type': 'online_notifier',
    #         'online_count': online_count
    #     }
    #     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
    #     return super().connect()

    # def disconnect(self, code):
    #     async_to_sync(self.channel_layer.group_discard)(self.chatroom_name, self.channel_name)
    #     # Decrease online users count
    #     self.chatroom.online_users.remove(self.user)
    #     # Broadcast online users count to all users active
    #     online_count = self.chatroom.online_users.count() - 1
    #     event = {
    #         'type': 'online_notifier',
    #         'online_count': online_count
    #     }
    #     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
    #     return super().disconnect(code)
    
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     body = text_data_json['body']
    #     message = GroupMessage.objects.create(
    #         body = body,
    #         author = self.user, 
    #         group = self.chatroom 
    #     )
    #     event = {
    #         'type': 'message_handler',
    #         'message_id': message.id
    #     }
    #     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
    #     # context = {
    #     #     "messages": [message],
    #     #     "user": self.user
    #     # }
    #     # html = render_to_string(template_name='chat/partials/bubbles.html', context=context)
    #     # self.send(text_data=html)

    # def message_handler(self, event):
    #     message_id = event['message_id']
    #     messages = GroupMessage.objects.filter(id=message_id)
    #     context = {
    #         "messages": messages,
    #         "user": self.user
    #     }
    #     html = render_to_string(template_name='chat/partials/bubbles.html', context=context)
    #     self.send(text_data=html)

    # def online_notifier(self, event):
    #     online_count = event['online_count']
    #     context = {
    #         'online_count': online_count
    #     }
    #     html = render_to_string(template_name='chat/partials/online_count.html', context=context)
    #     self.send(text_data=html)

