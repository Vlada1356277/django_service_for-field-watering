from django.contrib import admin

from .models import Device, User

# Register your models here.
admin.site.register(Device)
admin.site.register(User)