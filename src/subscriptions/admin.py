from django.contrib import admin
from subscriptions.models import Subscription, Price, UserSubscription

class PriceAdmin(admin.StackedInline):
    model = Price
    readonly_fields = ['price_id']
    # can_delete = False
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [PriceAdmin]
    list_display = ['name', 'active', 'featured']
    readonly_fields = ['product_id']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)