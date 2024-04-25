import uuid

from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    # поменять тип?
    phone = models.CharField(max_length=12, unique=True)
    auth_token = models.UUIDField(
        default=uuid.uuid4, verbose_name='Токен авторизации', auto_created=True, null=False, blank=False
    )
    devices = models.ManyToManyField('Device', related_name='users')

    def __str__(self):
        return self.name


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=12)
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=40)

    def __str__(self):
        return self.name
