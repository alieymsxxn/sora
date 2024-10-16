from django.urls import path
from subscriptions.views import pricing, cancel_subscription, refresh

urlpatterns = [
    path(route='pricing/<str:interval>/', view=pricing, name='pricing'),
    path(route='subscription/refresh/', view=refresh, name='refresh'),
    path(route='subscription/cancel/', view=cancel_subscription, name='cancel_subscription'),
]