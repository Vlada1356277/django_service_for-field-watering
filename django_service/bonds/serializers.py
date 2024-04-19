from rest_framework import serializers

from .models import Device, User


class DeviceSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    class Meta:
        model = Device
        fields = ('uuid', 'name')

