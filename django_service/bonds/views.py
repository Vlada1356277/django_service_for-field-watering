from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .models import Device
from .serializers import DeviceSerializer

class BondsAPIView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
# def index(request):
#     list = Device.objects.all()
#     return HttpResponse(list)

