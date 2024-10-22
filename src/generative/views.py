import json
from django.http import JsonResponse
from generative.scripts.facade import GenerationFacade

def generate_email(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body) 
        job_url = data['job_url']
        email = GenerationFacade.generate_email(url=job_url)
        data = {'email': email}
        return JsonResponse(data)
    return JsonResponse({'message': 'Invalid request', 'status': 'fail'}, status=400)

def generate_demo_email(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body) 
        job_url = data['job_url']
        services = data['services']
        email = GenerationFacade.generate_demo_email(url=job_url,services=services)
        data = {'email': email}
        return JsonResponse(data)
    return JsonResponse({'message': 'Invalid request', 'status': 'fail'}, status=400)