from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request=request, template_name='landing/landing.html')