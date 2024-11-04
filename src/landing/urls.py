from django.urls import path
from landing.views import landing


urlpatterns = [
    path(route='landing', view=landing, name='landing')
]