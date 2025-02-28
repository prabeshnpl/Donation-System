from django.shortcuts import HttpResponse


class CatchException:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        
        response = self.get_response(request)
        return response
        
    def process_exception(self,request,exception):
        print(exception)
        return HttpResponse(f'Sorry Error occured: {str(exception)}. Please report it to admin.')
