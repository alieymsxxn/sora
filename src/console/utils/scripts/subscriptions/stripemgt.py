import helpers
from customers.models import Customer
from django.db.models import Q
from subscriptions.models import UserSubscription


def cleanup_subs():
    customers = Customer.objects.filter(customer_id__isnull=False)
    for customer in customers:
        print(f'Cleaning up {customer.user} with {customer.customer_id}')
        listings = helpers.Billing.list_subscriptions(customer=customer.customer_id, status='active')
        subscriptions = [sub.id for sub in listings if sub.id != customer.user.usersubscription.mapped_id]
        for subscription in subscriptions:
            r = helpers.Billing.cancel_subscription(subscription_id=subscription, cancel_at_period_end=False)

def refresh_subs(user_ids=None):
    active_lookup = Q(status=UserSubscription.SubscriptionStatus.ACTIVE) | Q(status=UserSubscription.SubscriptionStatus.TRIALING)
    user_subscriptions = UserSubscription.objects.filter(active_lookup)
    if isinstance(user_ids, list):
        user_subscriptions = user_subscriptions.filter(user_id__in=user_ids)
    elif isinstance(user_ids, int):
        user_subscriptions = user_subscriptions.filter(user_id__in=[user_ids])
    elif isinstance(user_ids, str):
        user_subscriptions = user_subscriptions.filter(user_id__in=[user_ids])
    for user_subscription in user_subscriptions:
        print(f'Refreshing {user_subscription.user}')