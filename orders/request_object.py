from . import models
#https://docs.djangoproject.com/en/4.2/topics/http/middleware/ middle coding taken from django documentation
def RequestObjectMiddleWare(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        models.request_object = request

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware