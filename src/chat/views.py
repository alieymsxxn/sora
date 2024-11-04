from django.shortcuts import render
from django.contrib.auth import get_user_model
from chat.models import Message, Channel
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.http import Http404
User = get_user_model()

# Create your views here.
def chat(request):
    pass
    # if request.htmx:
    #     form = ChatmessageCreateForm(request.POST)
    #     if form.is_valid:
    #         message = form.save(commit=False)
    #         message.author = request.user
    #         message.group = ChatGroup.objects.get(name='Public Chat')
    #         message.save()
    #         context = {
    #             'author': message.author,
    #             'body': message.body, 
    #             'created': message.created
    #         }
    #         return render(request=request, template_name='chat/partials/bubble.html', context=context)
    # group = ChatGroup.objects.get(name='Public Chat')
    # messages = GroupMessage.objects.filter(group=group)[10:]
    # context = {
    #     'group': group,
    #     'messages': messages,
    #     'form': ChatmessageCreateForm
    # }
    # return render(request=request, template_name='chat/chat-box.html', context=context)
def channels(request, slug):
    if request.htmx:
        channel =  get_object_or_404(Channel, slug=slug)
        messages = Message.objects.filter(channel=channel)

        context = {
            'channel': channel,
            'messages': messages,
            'is_counsumer': False,
            "private_channel": False
        }
        return render(request=request, template_name='chat/dashboard/partials/message_box.html', context=context)

def private_channels(request, client_friend):
    if request.htmx:
        #  Extract sender and receiver username
        client, friend = client_friend.split('-')
        #  Check if both users are friends
        client = User.objects.get(username=client)
        # if not client.profile.friends.filter(username=friend).exists():
        #     return False
        #  Get or create their private channel
        friend = client if client.username == friend else User.objects.get(username=friend)
        members = {client.id, friend.id}
        private_channel = Channel.objects.filter(is_public=False, members__id__in=members).annotate(member_count=Count('members')).filter(member_count=len(members))
        if not private_channel:
            raise Http404("Channel is not available")
        private_channel = private_channel.get()
        # private_channel.members.
        #  Display their messages
        messages = Message.objects.filter(channel=private_channel)
        context = {
            'friend': friend,
            'channel': private_channel,
            'messages': messages,
            'is_counsumer': False,
        }
        return render(request=request, template_name='chat/dashboard/partials/message_box.html', context=context)

def dashboard(request):
    user = User.objects.get(id=request.user.id)
    friends = user.profile.friends.all()
    channels = user.profile.channels.all()

    context = {
        'friends': friends,
        'channels': channels,
    }
    return render(request=request, template_name='chat/dashboard/dashboard.html', context=context)