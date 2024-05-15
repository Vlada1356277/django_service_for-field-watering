import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import generics, status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import APIException

from .models import Device, Users
from .serializers import DeviceSerializer



class BondsAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   # mixins.CreateModelMixin,
                   GenericViewSet):
    # queryset = Device.objects.all()

    authentication_classes = [TokenAuthentication, SessionAuthentication]  # Add the authentication classes
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = user.devices.all()
        return queryset
    serializer_class = DeviceSerializer

    def add_device(self, request):
        if request.method == 'GET':
            return render(request, 'add_device.html')

    #  сделать открытым только для конкретного юзера\

    # def get_queryset(self):
    #     # Получение пользователя из запроса
    #     user = self.request.user
    #     queryset = Device.objects.filter(user=user)
    #     # Возврат только объектов для этого пользователя
    #     return queryset


class BindDeviceView(APIView):
    def get(self, request):
        serial_number = self.request.query_params.get('deviceSN')
        device_type = self.request.query_params.get('deviceType')
        user_auth_code = self.request.query_params.get('authCode')

        if serial_number is None:
            raise APIException(detail='GET параметер serial_number обязателен')

        if device_type is None:
            raise APIException(detail='GET параметер device_type обязателен')

        if user_auth_code is not None:
            users = Users.objects.filter(auth_token=user_auth_code)
            if not users.exists():
                raise APIException(detail='Пользователя с таким auth_token не существует')
            user = users.first()
            # user.devices.append(device)
            device, _ = Device.objects.get_or_create(uuid=serial_number[:12], defaults={"type": device_type[:40]})
            user.devices.add(device)
            user.save()
            # request fast-api-service/subscribe-mqtt?device_type=..&deviceSN=..

            return Response({'message': "Успешно добавлено устройство"}, status=status.HTTP_201_CREATED)
        else:
            b64 = base64.b64encode(
                (f'/devices/bind?deviceSN={serial_number}&deviceType={device_type}').encode('utf-8')
            ).decode('utf-8')
            return HttpResponseRedirect(
                redirect_to=f'/login?bindUrl={b64}'
            )
