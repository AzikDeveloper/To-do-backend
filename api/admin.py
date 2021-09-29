from django.contrib import admin
from .models import Task, ApiToken

admin.site.register(Task)
admin.site.register(ApiToken)
