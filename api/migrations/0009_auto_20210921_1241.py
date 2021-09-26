# Generated by Django 3.2.7 on 2021-09-21 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_alter_apitoken_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='apitoken',
            name='token',
            field=models.UUIDField(default=uuid.UUID('0a69e39b-d2a4-4cb6-9325-58ff039fdc42'), editable=False, unique=True),
        ),
    ]