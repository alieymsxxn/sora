from django.urls import path
from customers.views import profile

urlpatterns = [
    path(route='profile/', view=profile, name='profile'),
]