# Generated by Django 3.2.7 on 2021-09-30 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_apitoken_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApiToken',
        ),
    ]