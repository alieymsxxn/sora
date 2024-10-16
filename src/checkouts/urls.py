from django.urls import path
from checkouts.views import select_plan, checkout, success

urlpatterns = [
    path(route='select_plan/<str:price_id>/', view=select_plan, name='select_plan'),
    path(route='checkout/', view=checkout, name='checkout'),
    path(route='success/', view=success, name='success'),
]