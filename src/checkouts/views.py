import helpers
from django.shortcuts import render, redirect
from django.urls import reverse
from subscriptions.models import Price, Subscription, UserSubscription
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.
def select_plan(request, price_id):
    request.session['price_id'] = price_id
    return redirect('checkout')

@login_required
def checkout(request, *args, **kwargs):
    price_id = request.session.get('price_id')
    price = Price.objects.filter(id=price_id).first()
    if not price_id and not price:
        redirect('pricing')
    customer = request.user.customer.customer_id
    print('Price', price.price_id)
    print('Customer', customer)
    price = price.price_id
    customer = request.user.customer.customer_id
    success_url = settings.BASE_URL + reverse(viewname='success')
    cancel_url = settings.BASE_URL + reverse(viewname='pricing', kwargs={'interval': 'monthly'})
    rdir_url = helpers.Billing.start_session(customer=customer, 
                                  success_url=success_url,
                                  cancel_url=cancel_url,
                                  price=price)
    return redirect(rdir_url)

@login_required
def success(request, *args, **kwargs):
    session_id = request.GET['session_id']
    data = helpers.Billing.get_subscription_info(session_id=session_id)
    user = User.objects.get(id=request.user.id)
    price = Price.objects.get(price_id=data.pop('price_id'))
    subscription = price.subscription
    user_subscription = UserSubscription.objects.filter(user=user, active=True).first()
    if not user_subscription:
        user_subscription = UserSubscription(user=user)
    for attr, value in data.items():
        setattr(user_subscription, attr, value)
    user_subscription.subscription = subscription
    user_subscription.price = price
    user_subscription.save()    
    return redirect('profile')