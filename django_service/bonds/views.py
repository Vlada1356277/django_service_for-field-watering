from urllib.parse import urljoin

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from authorize.authentication import BearerTokenAuthentication
from django_service.settings import MQTT_SERVICE_URL
from .models import Device
from .serializers import DevicesSerializer, DeviceSerializer


class CanViewAllDevices(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class AllDevicesAPIView(APIView):
    permission_classes = [CanViewAllDevices]

    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response({'devices': serializer.data})


# миксины предоставляют базовую функциональность для работы с наборами данных (querysets)
class BondsAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = DevicesSerializer

    def get_queryset(self):
        user = self.request.user
        devices = Device.objects.filter(users=user)

        # Объединяем данные из FastAPI с устройствами
        enriched_devices = []
        for device in devices:
            fastapi_url = f"{MQTT_SERVICE_URL}{device.serial_number}"
            redirect_url = urljoin(MQTT_SERVICE_URL, f'devices/{device.serial_number}')
            response = requests.get(fastapi_url)

            if response.status_code == 200:
                fastapi_data = response.json()
                device_data = {
                    "serial_number": device.serial_number,
                    "name": device.name,
                    "temperature": fastapi_data.get("temperature", None),
                    "rssi": fastapi_data.get("rssi", None),
                    "redirect_url": redirect_url
                }
            else:
                device_data = {
                    "serial_number": device.serial_number,
                    "name": device.name,
                    "temperature": None,
                    "rssi": None,
                    "redirect_url": redirect_url
                }

            enriched_devices.append(device_data)

        return enriched_devices

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = self.request.user
        return render(request, 'devices.html', {'devices': queryset, 'user': user})

    def add_device(self, request):
        if request.method == 'GET':
            return render(request, 'add_device.html')

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            # device = self.get_object()
            # self.perform_destroy(device)
            # device = Device.objects.get(serial_number=pk)
            serial_number = kwargs.get('pk')
            try:
                device = Device.objects.get(serial_number=serial_number)
            except ObjectDoesNotExist:
                return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
            # device = self.request.

            response = requests.delete(
                MQTT_SERVICE_URL + "delete_device",
                json={"serial_number": serial_number}
            )

            if response.status_code == 200:
                device.delete()
                return Response({"message": f"Deleted device {device.serial_number}"}, status=response.status_code)
            else:
                return Response({"error": "Failed to delete from other service"}, status=response.status_code)


    def update(self, request, *args, **kwargs):
        serial_number = kwargs.get('pk')
        try:
            device = Device.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        # partial = kwargs.pop('partial', False)
        name = request.data.get('name')

        device.name = name
        device.save()

        return Response({"message": f"Updated device {device.serial_number}"})


class BindDeviceView(APIView):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # обрабатывает запрос после qr, подписка на mqtt
    def get(self, request):
        serial_number = self.request.query_params.get('deviceSN')
        device_name = self.request.query_params.get('deviceName')

        if serial_number is None:
            raise APIException(detail='GET параметер serial_number обязателен')

        if device_name is None:
            raise APIException(detail='GET параметер device_name обязателен')

        user = request.user
        if not user.is_authenticated:
            raise APIException(detail='Пользователь не аутентифицирован')

        device, created = Device.objects.get_or_create(
            serial_number=serial_number[:12],
            defaults={"name": device_name[:40]})

        if not user.devices.filter(serial_number=device.serial_number).exists():
            response = requests.post(
                MQTT_SERVICE_URL + "subscribe_mqtt",
                json={"serial_number": serial_number, "name": device_name}
            )

            if response.status_code != 200 and response.status_code != 201:
                return Response({'error': "запрос на /subscribe_mqtt не выполнен"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user.devices.add(device)
            user.save()

            return Response({'message': "Успешно добавлено устройство " + f'{serial_number}'},
                            status=status.HTTP_201_CREATED)

        return Response({'message': "Устройство " + f'{serial_number}' + " уже связано с пользователем " + f'{user}'},
                        status=status.HTTP_200_OK)


class DeviceDetailsView(APIView):
    authentication_classes = [BearerTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, device_sn: str):
        print(urljoin(MQTT_SERVICE_URL, f'devices/{device_sn}'))
        return HttpResponseRedirect(redirect_to=urljoin(MQTT_SERVICE_URL, f'devices/{device_sn}'))
