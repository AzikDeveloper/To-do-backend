from .models import ApiToken
import uuid


def getApiToken(request):
    token = ApiToken.objects.get(token=uuid.UUID(request.headers.get('api-token')))
    return token


def getUser(request):
    token = getApiToken(request)
    return token.user
