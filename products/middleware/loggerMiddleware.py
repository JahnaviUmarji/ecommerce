class LoggerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print(f'[Middleware] {request.path} - {request.method}')

        response = self.get_response(request)

        print(f'[Middleware] status code {response.status_code}')

        return response