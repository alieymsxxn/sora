from django.utils.deprecation import MiddlewareMixin
from subscriptions.models import UserSubscription

class SubscriptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'usersubscription'):
            user_subscription = user.usersubscription
            intervals = filter(lambda interval: user_subscription.price.interval == interval, user_subscription.price.Interval)
            interval = next(intervals, None)
            subscription = {
                'has_access': user_subscription.has_access,
                'amount_paid': user_subscription.price.price,
                'interval': interval.label,
                'plan': user_subscription.subscription.name,
                'currency': user_subscription.price.currency,
                'end': user_subscription.end,
                'cancelled': user_subscription.cancelled
            }
            user.subscription = subscription
        return None