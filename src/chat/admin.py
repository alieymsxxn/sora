from django.contrib import admin

from chat.models import Channel, Profile, Message

admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(Profile)
