import pathlib
from django.http import HttpResponse
from django.shortcuts import render
   
def home_page(request, *args, **kwargs):
    context = {
        'title': 'Big Title'
    }
    return render(request=request, template_name='home.html', context=context)