from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
from django.contrib.auth import login

from .forms import PhoneChannelForm, PhoneCodeForm

from bonds.models import Users
import requests


class Login(APIView):
    def get(self, request):
        form = PhoneChannelForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = PhoneChannelForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            channel = form.cleaned_data['channel']

            response = requests.post(
                'https://api-auth.bast-dev.ru/api/v1/auth/request-code/no-captcha',
                json={"phoneNumber": phone_number, "sendingChannel": channel}
            )
            if response.status_code != 200:
                return Response({'error': "internal error"})
            return HttpResponseRedirect(redirect_to='/send-code')
        else:
            return render(request, 'login.html', {'form': form})


# send code, receive jwt
class AuthToken(APIView):
    # authentication_classes = [BearerTokenAuthentication]
    # permission_classes = [AllowAny]
    def get(self, request):
        form = PhoneCodeForm()
        return render(request, 'send_code.html', {'form': form})

    def post(self, request):
        global token
        form = PhoneCodeForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']

            response = requests.post(
                'https://api-auth.bast-dev.ru/api/v1/auth/login',
                json={"phoneNumber": phone_number, "code": code}
            )
            if response.status_code != 200:
                return Response({'error': "internal error"}, status=status.HTTP_401_UNAUTHORIZED)

            response_data = response.json()
            jwt_token = response_data.get('jwt')
            registered = response_data.get('registered')

            requests.post(
                f'https://api-auth.bast-dev.ru/api/v1/auth/r',
                json={"phoneNumber": phone_number, "code": code}
            )

            if not registered:
                return Response({'error': 'You are not registered'})
            else:
                try:
                    # decode возвращает payload в виде словаря Python
                    # decoded_token = jwt.decode(jwt_token)
                    decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
                except jwt.DecodeError:
                    return Response({'error': 'Invalid token'})

            # ORM method tries to extract an object from the database based on the provided parameters, returns a tuple (object, bool)
            user, created = Users.objects.get_or_create(
                esiaId=decoded_token["esiaId"],
                defaults={"name": decoded_token["firstName"] + ' ' + decoded_token["lastName"]}
            )
            # if user:
            #     token, created = Token.objects.get_or_create(user=user)
            # сессия
            login(request, user)

            # return Response({'message': 'user authenticated'})
            # response = HttpResponseRedirect(redirect_to='/devices')
            # response.set_cookie('auth_token', token.key, httponly=True, secure=True)
            return HttpResponseRedirect(redirect_to='/devices')
