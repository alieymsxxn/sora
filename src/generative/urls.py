from django.urls import path
from generative.views import generate_email, generate_demo_email
urlpatterns = [
    # path('generate/email/', generate_email, name='generate_email'),
    path('generate/demo-email/', generate_demo_email, name='generate_demo_email'),
]