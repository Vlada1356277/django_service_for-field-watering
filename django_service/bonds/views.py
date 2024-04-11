from django.shortcuts import render
from django.http import HttpResponse

from .models import Device


def index(request):
    list = Device.objects.all()
    return HttpResponse(list)

