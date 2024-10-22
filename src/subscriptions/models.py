import helpers
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, pre_delete
from console.utils.mixins.models import TimeAuditMixin, PriorityMixin


User = settings.AUTH_USER_MODEL

PERMISSIONS = [
    ('advance', 'Advance Access'),
    ('basic', 'Basic Access'),
    ('trial', 'Trial Access'),
]


class Subscription(TimeAuditMixin, PriorityMixin):
    '''
    Stripe Product
    '''
    class Meta:
        permissions = PERMISSIONS
        ordering = ['order', 'featured']

    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission,
                                         limit_choices_to={
                                             'content_type__app_label': 'subscriptions',
                                             'codename__in': [x[0] for x in PERMISSIONS],
                                        })
    product_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    features = models.TextField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwags) -> None:
        product_id = helpers.Billing.get_or_create_product(name=self.name)
        setattr(self, 'product_id', product_id)
        return super().save(*args, **kwags)

    def __str__(self):
        return f'{self.name}'


class Price(TimeAuditMixin, PriorityMixin):
    '''
    Stripe Price
    '''
    class Interval(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'
        WEEKLY = 'week', 'Weekly'

    class Meta:
        ordering = ['order', 'featured']

    subscription = models.ForeignKey(to=Subscription, null=True, on_delete=models.SET_NULL, related_name='price')
    price_id = models.CharField(max_length=100, null=True, blank=True)
    interval = models.CharField(max_length=100, default=Interval.MONTHLY, choices=Interval.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)

    @property
    def get_checkout_url(self):
        return reverse(viewname='select_plan', kwargs={'price_id': self.id})

    @property
    def description(self):
        if self.subscription:
            return self.subscription.description
        return None

    @property
    def features(self):
        if self.subscription:
            return [feature.strip() for feature in self.subscription.features.split('\n')]
        return None

    @property
    def name(self):
        if self.subscription:
            return self.subscription.name
        return 'Pricing'

    @property
    def currency(self):
        return 'usd'

    @property
    def unit_amount(self):
        return int(self.price * 100)

    @property
    def product_id(self):
        return self.subscription.product_id if self.subscription else None

    @property
    def product_status(self):
        return self.subscription.active if self.subscription else False

    def __str__(self) -> str:
        return f'${self.price} per {self.interval}'

    def save(self, *args, **kwargs) -> None:
        # Create a price on Stripe
        if self.product_id and self.product_status:
            price_id = helpers.Billing.get_or_create_price(currency=self.currency,
                                                           unit_amount=self.unit_amount,
                                                           recurring={ 'interval': self.interval },
                                                           product=self.product_id)
            if not Price.objects.filter(subscription=self.subscription, 
                                        price_id=self.price_id) \
                                        .exclude(id=self.id).exists():
                setattr(self, 'price_id', price_id)
        if self.featured:
            other = Price.objects.filter(interval=self.interval, 
                                        subscription=self.subscription) \
                                        .exclude(id=self.id)
        return super().save(*args, **kwargs)


class UserSubscription(models.Model):

    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRIALING = 'trialing', 'Trialing'
        INCOMPLETE = 'incomplete', 'Incomplete'
        INCOMPLETE_EXPIRED = 'incomplete_expired', 'Incomplete Expired'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELED = 'canceled', 'Canceled'
        UNPAID = 'unpaid', 'Unpaid'
        PAUSED = 'paused', 'Paused'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    mapped_id = models.CharField(max_length=100, null=False)
    price = models.ForeignKey(to=Price, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, null=True, blank=True, choices=SubscriptionStatus.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_start = models.DateTimeField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    cancelled = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.user.username} - {self.subscription}'

    @property
    def has_access(self):
        if self.status and self.status in [self.SubscriptionStatus.ACTIVE, self.SubscriptionStatus.TRIALING]:
            return True
        return False

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            old = UserSubscription.objects.get(pk=self.pk)
            if old.mapped_id != self.mapped_id:
                helpers.Billing.cancel_subscription(subscription_id=old.mapped_id)
        else:
            self.first_start = self.start
        return super().save(*args, **kwargs)

    def refresh(self):
        info = helpers.Billing.get_subscription_info(subscription_id=self.mapped_id)
        price = Price.objects.filter(price_id=info.pop('price_id')).first()
        self.price = price
        for attr, value in info.items():
            setattr(self, attr, value)
        self.save()


@receiver(signal=post_save, sender=UserSubscription)
def instate(instance, *args, **kwargs):
    user = instance.user
    groups = instance.subscription.groups.all()
    if not instance.active or kwargs.get('revoke', False):
        return user.groups.remove(*groups)
    groups = groups | user.groups.all()
    user.groups.set(groups)
# post_save.connect(receiver=sync_user, sender=UserSubscription)


@receiver(signal=pre_delete, sender=UserSubscription)
def revoke(sender, instance, **kwargs):
    instate(sender=sender, instance=instance, revoke=True)
# pre_delete.connect(receiver=revoke, sender=UserSubscription)
