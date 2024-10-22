"""
URL configuration for sora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('signin/', allauth_views.login, name='login'),
    # path('signup/', allauth_views.signup, name='signup'),
    # path('logout/', allauth_views.logout, name='logout'),
    # path('confirm-email/', allauth_views.confirm_email, name='confirm_email'),
    # path('github/login/', oauth2_login, name='github-login'),
    path('', include('landing.urls')),
    path('', include('generative.urls')),
    path('', include('dashboard.urls')),
    # path('', include('visits.urls')), # index page / root page
    path('', include('checkouts.urls')),
    path('', include('customers.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('subscriptions.urls')),
    path('admin/', admin.site.urls),
]
