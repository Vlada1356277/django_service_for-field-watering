from rest_framework import serializers


class AuthSendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)
    channel_type = serializers.CharField()


class AuthGetToken(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)
    code = serializers.CharField(max_length=6)
