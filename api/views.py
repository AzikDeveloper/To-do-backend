from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from .forms import CreateUserForm
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def testApiView(request):
    return Response('Access granted!')


@api_view(['POST'])
def registerView(request):
    print(request.headers)
    form = CreateUserForm(request.data)
    if form.is_valid():
        form.save()
        response = {
            'ok': 'true',
            'detail': 'password and username are valid'
        }
        return Response(response)
    else:
        print(form.errors.as_text())
        response = {
            'ok': 'true',
            'detail': 'username is already taken or password and username are not valid'
        }
        return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def logOutView(request):
    try:
        refreshToken = request.data['refresh_token']
        token = RefreshToken(refreshToken)
        token.blacklist()
        return Response({
            'ok': 'true'
        })
    except Exception:
        return Response({
            'ok': 'false',
            'detail': 'bad request'
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changeProfileView(request):
    user = request.user
    form = CreateUserForm(instance=user, data=request.data)
    if form.is_valid():
        form.save()
        response = {
            'ok': 'true',
            'detail': 'username and password are valid',
            'username': user.username
        }
        return Response(response)
    else:
        response = {
            'ok': 'false',
            'detail': 'username is already taken or password and username are not valid'
        }
        return Response(response)


@api_view(['GET'])
def apiOverView(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',

    }
    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def tasksListView(request):
    user = request.user
    tasks = user.task_set.filter(deleted=bool(request.data['deleted'])).order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    response = {
        'ok': 'true',
        'reason': 'successful process',
        'data': serializer.data,
        'username': user.username
    }
    return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def taskCreateView(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        response = {
            'ok': 'true',
            'reason': 'successful process',
            'data': serializer.data
        }
        return Response(response)
    else:
        response = {
            'ok': 'false',
            'reason': 'invalid credentials'
        }
        return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateReminder(request):
    try:
        task = request.user.task_set.get(id=request.data.get('id'))
        task.reminder = not task.reminder
        task.save()

        response = {
            'ok': 'true',
            'detail': 'successful process',
            'reminder': task.reminder
        }
        return Response(response)
    except ObjectDoesNotExist:
        response = {
            'ok': 'false',
            'detail': 'task not found'
        }
        return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def taskUpdateView(request):
    data = request.data.copy()
    data['user'] = request.user.id
    task = request.user.task_set.get(id=request.data.get('id'))
    serializer = TaskSerializer(instance=task, data=data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'ok': 'true',
            'detail': 'successful process',
            'data': serializer.data
        }
        return Response(response)
    else:
        response = {
            'status': 'not ok',
            'reason': 'invalid credentials'
        }
        return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def taskDeleteView(request):
    print('>>', request.data)
    try:
        task = request.user.task_set.get(id=request.data.get('id'))
        task.delete()
        response = {
            'ok': 'true',
            'detail': 'successful process'
        }
        return Response(response)
    except ObjectDoesNotExist:
        response = {
            'ok': 'false',
            'detail': 'task not found'
        }
        return Response(response)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteTasksView(request):
    request.user.task_set.filter(deleted=True).delete()
    response = {
        'ok': 'true'
    }
    return Response(response)
