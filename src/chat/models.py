import shortuuid
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Channel(models.Model):
    name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    online_users = models.ManyToManyField(to=User, blank=True, related_name='online_members')
    members = models.ManyToManyField(to=User, related_name='memebers', blank=True)
    owner = models.ForeignKey(to=User, related_name='owner', null=True, blank=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    friends = models.ManyToManyField(to=User, default=None, related_name='friends')
    channels = models.ManyToManyField(to=Channel, default=None, related_name='users')

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(to=User, related_name='sender', null=True, on_delete=models.SET_NULL)
    reciever = models.ForeignKey(to=User, related_name='reciever', null=True, blank=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey(to=Channel, related_name='channel', null=True, on_delete=models.SET_NULL)
    body = models.CharField(max_length=200, null=False, blank=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.body
    
from django.db.models.signals import post_save, pre_delete
from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver

@receiver(signal=post_save, sender=User)
def create_profile(instance, *args, **kwargs):
    if not instance.profile:
        Profile(user=instance).save()

# def signup(request, user, *args, **kwargs):
#     Customer(
#         user=user,
#         email=user.email,
#     ).save()
# user_signed_up.connect(receiver=signup)
