from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

def dashboard(request):
    return render(request=request, template_name='dashboard/main.html')