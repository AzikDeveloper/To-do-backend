from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', apiOverView, name='api'),
    path('tasks-list/', tasksListView, name='tasks_list'),
    path('task-create/', taskCreateView, name='task_create'),
    path('update-task/', taskUpdateView, name='task_update'),
    path('task-delete/', taskDeleteView, name='task_delete'),
    path('logout/', logOutView, name='logout'),
    path('change-profile/', changeProfileView, name='change_profile'),
    path('register/', registerView, name='register'),
    path('update_reminder/', updateReminder, name='update_reminder'),
    path('delete-tasks/', deleteTasksView, name='delete_tasks'),
    path('test-api/', testApiView, name='test')
]