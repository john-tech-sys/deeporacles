import logging
from django.shortcuts import render
from django.http import HttpResponseNotFound

logger = logging.getLogger(__name__)

class HandleAllExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the exception
        logger.error(f'Unhandled exception: {exception}', exc_info=True)
        # Return custom 404 page
        return HttpResponseNotFound(render(request, 'home/404.html'))
