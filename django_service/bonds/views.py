from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .models import Device
from .serializers import DeviceSerializer
from rest_framework.permissions import IsAuthenticated

class BondsAPIView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for this viewset

    def get_queryset(self):
        # Filter queryset to include only devices owned by the authenticated user
        return self.queryset.filter(user=self.request.user)

# def index(request):
#     list = Device.objects.all()
#     return HttpResponse(list)

