from django.urls import path
from .views import *


urlpatterns = [
    path('', apiOverView, name='api'),
    path('tasks-list/', tasksListView, name='tasks_list'),
    path('task-detail/<str:pk>', taskDetailView, name='task_detail'),
    path('task-create/', taskCreateView, name='task_create'),
    path('update-task', taskUpdateView, name='task_update'),
    path('task-delete/<str:pk>', taskDeleteView, name='task_delete'),
    path('login/', loginView, name='login'),
    path('logout/', logOutView, name='logout'),
    path('change-profile/', changeProfileView, name='change_profile'),
    path('register/', registerView, name='register'),
    path('update_reminder/', updateReminder, name='update_reminder')
]