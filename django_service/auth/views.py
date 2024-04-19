import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from auth.serializers import AuthSendCodeSerializer, AuthGetToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from bonds.models import User


# receive code
class AuthCode(APIView):
    def post(self, request):
        serializer = AuthSendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not validated_data['channel_type'] in ['Sms', 'Telegram', 'Whatsapp']:
            return JsonResponse(status=401, data={'error': "Неверное значение channel_type"})

        resp = requests.post(
            'https://api-auth.bast-dev.ru/api/v1/auth/request-code/no-captcha',
            json={"phoneNumber": validated_data['phone_number'], "sendingChannel": validated_data['channel_type']}
        )

        if resp.status_code != 200:
            return JsonResponse(status=401, data={'error': "internal error"})

        return JsonResponse(status=200, data={'detail': "Please wait for auth code"})


# send code, receive jwt
class AuthToken(APIView):
    def post(self, request):
        serializer = AuthGetToken(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        resp = requests.post(
            'https://api-auth.bast-dev.ru/api/v1/auth/login',
            json={"phoneNumber": validated_data['phone_number'], "code": validated_data['code']}
        )

        if resp.status_code != 200:
            return JsonResponse(status=401, data={'error': "internal error"})

        response_data = resp.json()
        jwt_token = response_data.get('jwt')
        # registered = response_data.get('registered')
        # regToken = response_data.get('registrationToken')

        try:
            decoded_token = jwt.decode(jwt_token, options={"verify_signature": False, "verify_exp": False})
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'})

        user, _ = User.objects.get_or_create(
            phone=decoded_token["phoneNumber"],
            defaults={"name": decoded_token["firstName"] + ' ' + decoded_token["lastName"]}
        )

        # Return the decoded JWT in the response
        return Response({'auth_token': user.auth_token}, status=status.HTTP_200_OK)


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')
