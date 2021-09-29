from rest_framework.views import Response
from .models import ApiToken
from django.core.exceptions import ObjectDoesNotExist
import uuid


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        api_token = request.headers.get('api-token')
        if api_token != 'null':
            try:
                token = ApiToken.objects.get(token=uuid.UUID(api_token))
                return view_func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                response = {
                    'status': 'not ok',
                    'reason': 'token is not found'
                }
                return Response(response)
        else:
            response = {
                'status': 'not ok',
                'reason': 'api-token is null',
            }
            return Response(response)

    return wrapper
