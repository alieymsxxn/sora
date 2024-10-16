import helpers
from django.db import models
from django.conf import settings
from allauth.account.signals import user_signed_up, email_confirmed

User = settings.AUTH_USER_MODEL

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User, null=True, on_delete=models.SET_NULL)
    customer_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, default=None)
    verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    phone_number = models.CharField(max_length=100, default='', blank=True)

    def save(self, *args, **kwargs) -> None:
        # Associate a cutsomer id if doesnt exist
        if self.verified and self.email:
            customer_id = helpers.Billing.get_or_create_customer(email=self.email,
                                                                 name=self.user.username)
            self.customer_id = customer_id
        return super().save(*args, **kwargs)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'.strip( )

    def __str__(self) -> str:
        return f"{self.user}"


def signup(request, user, *args, **kwargs):
    Customer(
        user=user,
        email=user.email,
    ).save()
user_signed_up.connect(receiver=signup)


def verification(request, email_address, *args, **kwargs):
    for customer in Customer.objects.filter(email=email_address, verified=False):
        customer.verified = True
        customer.save()
email_confirmed.connect(receiver=verification)
