from django.http import HttpResponse
from django.utils import simplejson

""" Core functions for the site that are used frequently """

def json_response(data, error=False, **kwargs):
    response = HttpResponse(simplejson.dumps(data), mimetype = 'application/json', ** kwargs)
    if error:
        response.status_code = 400

    return response
