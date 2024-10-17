from django.urls import path
from landing.views import landing


urlpatterns = [
    path(route='', view=landing, name='landing')
]