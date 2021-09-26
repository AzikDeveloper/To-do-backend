from django.db import models
from django.contrib.auth.models import User
import uuid


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=200, null=True)
    day = models.DateTimeField(null=True)
    reminder = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class ApiToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)

    def __str__(self):
        return f'token({self.id})'