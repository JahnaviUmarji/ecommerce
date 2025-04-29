from json import *
class SecondMiddleware:
    def __init__(self,get_reponse):
        self.get_reponse = get_reponse

    def __call__(self, request):
        
        json_data = getattr(request, 'custom_data', {})

        try:
            data = loads(json_data)
            print(f"[First Middleware data from Second Middleware] - Path: {data.get('path')}, Method: {data.get('method')}")

        except JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")

        response = self.get_reponse(request)

        print(f"[Second Middleware] status code {response.status_code}")

        return response