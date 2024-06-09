import os
from urllib.parse import urljoin

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from authorize.authentication import BearerTokenAuthentication
from .models import Device
from .serializers import DevicesSerializer

load_dotenv(find_dotenv())

service_url = os.getenv('MQTT_SERVICE_URL')


class BondsAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = DevicesSerializer

    def get_queryset(self):
        # user = self.request.user
        # # queryset = user.devices.all()
        # # return queryset
        # return Device.objects.filter(users=user)
        user = self.request.user
        devices = Device.objects.filter(users=user)

        # Объединяем данные из FastAPI с устройствами
        enriched_devices = []
        for device in devices:
            fastapi_url = f"{service_url}{device.serial_number}"
            response = requests.get(fastapi_url)

            if response.status_code == 200:
                fastapi_data = response.json()
                device_data = {
                    "serial_number": device.serial_number,
                    "name": device.name,
                    "temperature": fastapi_data.get("temperature", None),
                    "rssi": fastapi_data.get("rssi", None)
                }
            else:
                device_data = {
                    "serial_number": device.serial_number,
                    "name": device.name,
                    "temperature": None,
                    "rssi": None
                }

            enriched_devices.append(device_data)

        return enriched_devices

    def add_device(self, request):
        if request.method == 'GET':
            return render(request, 'add_device.html')

    # def retrieve(self, request, *args, **kwargs):
    #     serial_number = kwargs.get('pk')
    #     device = get_object_or_404(self.get_queryset(), serial_number=serial_number)
    #
    #     fastapi_url = f"{service_url}{serial_number}"
    #
    #     response = requests.get(fastapi_url)
    #
    #     if response.status_code == 200:
    #         return JsonResponse(response.json())
    #     else:
    #         return HttpResponseNotFound("Device not found")


class BindDeviceView(APIView):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # обрабатывает запрос после qr, подписка на mqtt
    def get(self, request):
        serial_number = self.request.query_params.get('deviceSN')
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
            serial_number=serial_number[:12],
            defaults={"name": device_name[:40]})

        if not user.devices.filter(serial_number=device.serial_number).exists():
            response = requests.post(
                service_url + "subscribe_mqtt",
                json={"serial_number": serial_number, "name": device_name}
            )

            if response.status_code != 200 and response.status_code != 201:
                return Response({'error': "запрос на /subscribe_mqtt не выполнен"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user.devices.add(device)
            user.save()

            return Response({'message': "Успешно добавлено устройство " + f'{serial_number}'},
                            status=status.HTTP_201_CREATED)

        return Response({'message': "Устройство " + f'{serial_number}' + "уже связано с пользователем " + f'{user}'},
                        status=status.HTTP_200_OK)

class DeviceDetailsView(APIView):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, device_sn: str):
        print(urljoin(MQTT_SERVICE_URL, f'devices/{device_sn}'))
        return HttpResponseRedirect(redirect_to=urljoin(MQTT_SERVICE_URL, f'devices/{device_sn}'))