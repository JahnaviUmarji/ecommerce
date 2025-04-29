from json import *
class FirstMiddleware:
    def __init__(self,get_reponse):
        self.get_reponse = get_reponse

    def __call__(self,request):
        print(f"[First Middleware] {request.path} - {request.method}")

        data = {
            'path': request.path,
            'method': request.method
        }

        request.custom_data = dumps(data)

        response = self.get_reponse(request)

        print(f"[First Middleware] status code {response.status_code}")

        return response

