from django.utils.deprecation import MiddlewareMixin
from subscriptions.models import UserSubscription

class ProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            user.first_name = user.customer.first_name
            user.last_name = user.customer.last_name
            user.name = user.customer.name
            user.phone = user.customer.phone_number

        return None