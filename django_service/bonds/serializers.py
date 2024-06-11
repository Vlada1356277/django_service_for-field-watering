from rest_framework import serializers

from .models import Device, Users


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'esiaId', 'devices', 'is_staff', 'last_login', 'is_active']


class DevicesSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=100, allow_null=True)
    name = serializers.CharField(max_length=100)
    temperature = serializers.CharField(required=False, allow_null=True)
    rssi = serializers.CharField(required=False, allow_null=True)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40)
    esiaId = serializers.CharField(max_length=40, allow_null=False, default='')
    is_staff = serializers.BooleanField(default=False)
    last_login = serializers.DateTimeField()
    is_active = serializers.BooleanField(default=True)
