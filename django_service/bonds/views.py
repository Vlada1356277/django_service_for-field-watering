import base64

import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import generics, status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from authorize.authentication import BearerTokenAuthentication
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
                   GenericViewSet):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = DeviceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.devices.all()
        return queryset

    def add_device(self, request):
        if request.method == 'GET':
            return render(request, 'add_device.html')


class BindDeviceView(APIView):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serial_number = self.request.query_params.get('deviceId')
        device_name = self.request.query_params.get('deviceName')
        # user_auth_code = self.request.query_params.get('authCode')

        if serial_number is None:
            raise APIException(detail='GET параметер serial_number обязателен')

        if device_name is None:
            raise APIException(detail='GET параметер device_name обязателен')

        # users = Users.objects.filter(auth_token=user_auth_code)
        user = request.user
        if not user.is_authenticated:
            raise APIException(detail='Пользователь не аутентифицирован')

        # if not users.exists():
        #     raise APIException(detail='Пользователя с таким auth_token не существует')
        # user = users.first()
        device, created = Device.objects.get_or_create(
            uuid=serial_number[:12],
            defaults={"name": device_name[:40]})

        if not user.devices.filter(id=device.id).exists():
            response = requests.post(
                'http://127.0.0.1:8001/subscribe_mqtt',
                json={"serial_number": serial_number, "name": device_name}
            )

            if response.status_code != 200 and response.status_code != 201:
                return Response({'error': "запрос на /subscribe_mqtt не выполнен"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user.devices.add(device)
            user.save()

            return Response({'message': "Успешно добавлено устройство " + f'{serial_number}'},
                            status=status.HTTP_201_CREATED)

        return Response({'message': "Устройство " + f'{serial_number}' + "уже связано с пользователем " + f'{user}'},
                        status=status.HTTP_200_OK)
        # user = users.first()
        # device, _ = Device.objects.get_or_create(uuid=serial_number[:12], defaults={"type": device_type[:40]})
        # user.devices.add(device)
        # user.save()
        # # поменять localhost
        #
        # response = requests.post(
        #     'http://127.0.0.1:8001/subscribe_mqtt',
        #     json={"device_type": device_type, "serial_number": serial_number}
        # )
        #
        # if response.status_code != 200 and response.status_code != 201:
        #     return Response({'error': "internal error"})
        #
        # return Response({'message': "Успешно добавлено устройство " + f'{serial_number}'}, status=status.HTTP_201_CREATED)
    # else:
    #     b64 = base64.b64encode(
    #         (f'/devices/bind?deviceSN={serial_number}&deviceType={device_type}').encode('utf-8')
    #     ).decode('utf-8')
    #     return HttpResponseRedirect(
    #         redirect_to=f'/login?bindUrl={b64}'
    #     )
