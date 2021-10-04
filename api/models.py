from django.db import models
from django.contrib.auth.models import User
import uuid


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=200, null=True)
    day = models.DateTimeField(null=True)
    reminder = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.text



