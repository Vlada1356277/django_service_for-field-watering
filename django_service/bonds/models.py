import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from bonds.managers import UserManager


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True)
    esiaId = models.CharField(max_length=40, null=False, default='')
    devices = models.ManyToManyField('Device', related_name='users')
    # auth_code = models.CharField(max_length=40, default='')

    # потом установить, когда не нужна будет админка джанго уже:
    # password = None
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def __str__(self):
        return self.name


class Device(models.Model):
    # id = models.AutoField(primary_key=True)
    serial_number = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
