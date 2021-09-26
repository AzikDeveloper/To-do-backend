from rest_framework.views import Response
from .models import ApiToken
from django.core.exceptions import ObjectDoesNotExist
import uuid


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            api_token = request.headers.get('api-token')
            if api_token != 'null':
                token = ApiToken.objects.get(token=uuid.UUID(api_token))
                if token:
                    return view_func(request, *args, **kwargs)
                else:
                    print('not logged')
                    return Response('not-logged')
            else:
                return Response('not-logged')
        except ObjectDoesNotExist:
            print('not logged')
            return Response('not-logged')
    return wrapper
