from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
@login_required
def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        customer = request.user.customer
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone_number = phone
        customer.save()
        return redirect('profile')
    return render(request=request, template_name='customers/profile.html')