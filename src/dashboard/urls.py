from django.urls import path
from dashboard.views import dashboard

urlpatterns = [
    path(route='dashboard/', view=dashboard, name='dashboard')
]