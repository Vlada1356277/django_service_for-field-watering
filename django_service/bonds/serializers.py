from rest_framework import serializers

from .models import Device, Users


class DeviceSerializer(serializers.ModelSerializer):
    serial_number = serializers.UUIDField(read_only=True)
    class Meta:
        model = Device
        fields = ('serial_number', 'name')

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'esiaId', 'devices', 'is_staff', 'last_login', 'is_active']


class DevicesSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    temperature = serializers.CharField(required=False, allow_null=True)
    rssi = serializers.CharField(required=False, allow_null=True)
