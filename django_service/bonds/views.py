import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import APIException

from .models import Device, User
from .serializers import DeviceSerializer

#
class BondsAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   # mixins.CreateModelMixin,
                   GenericViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# # for GET and POST
# class BondsAPIView(generics.ListAPIView):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#     # permission_classes = [IsAuthenticated]  # FOR AUTH (+ in settings)
#
# # CRUD
# class BondsUpdate(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer


class BindDeviceView(APIView):
    def get(self, request):
        serial_number = self.request.query_params.get('deviceSN')
        device_type = self.request.query_params.get('deviceType')
        user_auth_code = self.request.query_params.get('authCode')

        if serial_number is None:
            raise APIException(detail='GET параметер serial_number обязателен')

        if device_type is None:
            raise APIException(detail='GET параметер device_type обязателен')

        device, _ = Device.objects.get_or_create(uuid=serial_number[:12], defaults={"type": device_type[:40]})

        if user_auth_code is not None:
            users = User.objects.filter(auth_token=user_auth_code)
            if not users.exists():
                raise APIException(detail='Пользователя с таким auth_token не существует')
            user = users.first()
            # user.devices.append(device)
            user.devices.add(device)
            user.save()

            return HttpResponse(status=201)
        else:
            return HttpResponseRedirect(redirect_to='/login')

