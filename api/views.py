from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from .decorators import login_required
from django.contrib.auth import authenticate
from .my_tools import *
from .forms import CreateUserForm
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'])
def registerView(request):
    form = CreateUserForm(request.data)
    if form.is_valid():
        form.save()
        response = {
            'status': 'ok',
            'reason': 'password and username are valid'
        }
        return Response(response)
    else:
        response = {
            'status': 'not ok',
            'reason': 'username is already taken or password and username are not valid'
        }
        return Response(response)


@api_view(['POST'])
def loginView(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        try:
            new_token = ApiToken.objects.create(user=user)
        except Exception:
            token = ApiToken.objects.get(user=user)
            token.delete()
            new_token = ApiToken.objects.create(user=user)
        response = {
            'status': 'ok',
            'reason': 'username and password is correct',
            'token': new_token.token,
            'username': user.username
        }
        return Response(response)
    else:
        response = {
            'status': 'not ok',
            'reason': 'username or password is not correct'
        }
        return Response(response)


@api_view(['POST'])
@login_required
def logOutView(request):
    token = getApiToken(request)
    token.delete()
    response = {
        'status': 'ok',
        'reason': 'successful process in logout'
    }
    return Response(response)


@api_view(['POST'])
@login_required
def changeProfileView(request):
    user = getUser(request)
    form = CreateUserForm(instance=user, data=request.data)
    if form.is_valid():
        form.save()
        response = {
            'status': 'ok',
            'reason': 'username and password are valid',
            'username': user.username
        }
        return Response(response)
    else:
        response = {
            'status': 'not ok',
            'reason': 'username is already taken or password and username are not valid'
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


@api_view(['GET'])
@login_required
def tasksListView(request):
    user = getUser(request)
    tasks = user.task_set.order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    response = {
        'status': 'ok',
        'reason': 'successful process',
        'data': serializer.data,
        'username': user.username
    }
    return Response(response)


@api_view(['GET'])
def taskDetailView(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@login_required
def taskCreateView(request):
    data = request.data.copy()
    data['user'] = getUser(request).id
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'status': 'ok',
            'reason': 'successful process',
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
@login_required
def updateReminder(request):
    task_id = request.data.get('task_id')
    try:
        task = Task.objects.get(id=task_id)
        task.reminder = not task.reminder
        task.save()

        response = {
            'status': 'ok',
            'reason': 'successful process',
            'reminder': task.reminder
        }
        return Response(response)
    except ObjectDoesNotExist:
        response = {
            'status': 'not ok',
            'reason': 'task not found'
        }
        return Response(response)


@api_view(['POST'])
def taskUpdateView(request):
    data = request.data.copy()
    data['user'] = getUser(request).id
    task = Task.objects.get(id=data['id'])
    serializer = TaskSerializer(instance=task, data=data)
    if serializer.is_valid():
        serializer.save()
        response = {
            'status': 'ok',
            'reason': 'successful process',
            'data': serializer.data
        }
        return Response(response)
    else:
        response = {
            'status': 'not ok',
            'reason': 'invalid credentials'
        }
        return Response(response)


@api_view(['DELETE'])
@login_required
def taskDeleteView(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task.delete()

        response = {
            'status': 'ok',
            'reason': 'successful process'
        }
        return Response(response)
    except ObjectDoesNotExist:
        response = {
            'status': 'not ok',
            'reason': 'task not found'
        }
        return Response(response)



