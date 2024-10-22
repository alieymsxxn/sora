from django.shortcuts import render, redirect
import helpers
from subscriptions.models import Price
from django.views.decorators.http import require_POST

@require_POST
def cancel_subscription(request):
    subscription_id = request.user.usersubscription.mapped_id
    cancel = helpers.Billing.cancel_subscription(subscription_id=subscription_id)
    return redirect(to='refresh')

def refresh(request):
    request.user.usersubscription.refresh()
    return redirect(to='profile')

def pricing(request, interval):
    for price_interval in Price.Interval:
        # redirect with monthly set as interval
        if price_interval.label.lower() == interval:
            interval = price_interval
            break
    if type(price_interval) is str:
        interval = Price.Interval.MONTHLY

    prices = Price.objects.filter(featured=True).filter(interval=interval)
    context = {
        'intervals': [interval.label.lower() for interval in Price.Interval],
        'interval': interval.label.lower(),
        'prices': prices,
        # 'monthly': featured.filter(interval=Price.Interval.MONTHLY),
        # 'yearly': featured.filter(interval=Price.Interval.YEARLY)
    }
    return render(request=request, template_name='subscriptions/pricing.html', context=context)