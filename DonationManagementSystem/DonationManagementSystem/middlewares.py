from django.shortcuts import HttpResponse,redirect
from django.contrib import messages
import logging,traceback

logger = logging.getLogger('django')
class CatchException:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        
        response = self.get_response(request)
        return response
        
    def process_exception(self,request,exception):

        logger.error("An error occurred: %s", str(exception))
        logger.error("\n\n\n"+traceback.format_exc()+"\n\n\n")

        messages.error(request,str(exception))
        return redirect('UserManagement:error')
