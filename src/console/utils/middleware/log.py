from django.http import HttpRequest, HttpResponse

class EssentialLogs:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        print('Preprocess - Essential Logs')
        response = self.get_response(request)
        print('Postprocess - Essential Logs')
        return response