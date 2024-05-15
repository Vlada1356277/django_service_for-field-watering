import base64

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
        bind_url = request.query_params.get('bindUrl')
        form = PhoneChannelForm(initial={'bind_url': bind_url if bind_url is not None else ''})
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = PhoneChannelForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            channel = form.cleaned_data['channel']
            bind_url = form.cleaned_data['bind_url']
            # Далее обработка отправки запроса
            response = requests.post(
                'https://api-auth.bast-dev.ru/api/v1/auth/request-code/no-captcha',
                json={"phoneNumber": phone_number, "sendingChannel": channel}
            )
            if response.status_code != 200:
                return Response({'error': "internal error"}, status=status.HTTP_401_UNAUTHORIZED)
            # return JsonResponse(status=200, data={'detail': "Please wait for auth code"})
            if bind_url is not None and bind_url.strip() != '':
                return HttpResponseRedirect(redirect_to=f'/send-code?bindUrl={bind_url}')
            return HttpResponseRedirect(redirect_to='/send-code')
        else:
            return render(request, 'login.html', {'form': form})


# send code, receive jwt
class AuthToken(APIView):
    def get(self, request):
        bind_url = request.query_params.get('bindUrl')
        # print('bind_url = ', bind_url)
        form = PhoneCodeForm(initial={'bind_url': bind_url if bind_url is not None else ''})
        return render(request, 'send_code.html', {'form': form})

    def post(self, request):
        form = PhoneCodeForm(request.POST)
        if form.is_valid():
            # country_code = form.cleaned_data['country_code']
            phone_number = form.cleaned_data['phone_number']
            code = form.cleaned_data['code']
            bind_url = form.cleaned_data['bind_url']

            response = requests.post(
                'https://api-auth.bast-dev.ru/api/v1/auth/login',
                json={"phoneNumber": phone_number, "code": code}
            )
            if response.status_code != 200:
                return Response({'error': "internal error"}, status=status.HTTP_401_UNAUTHORIZED)

            response_data = response.json()
            jwt_token = response_data.get('jwt')
            registered = response_data.get('registered')

            if not registered:
                return Response({'error': 'You are not registered'})
            else:
                try:
                    decoded_token = jwt.decode(jwt_token, options={"verify_signature": False, "verify_exp": False})
                except jwt.DecodeError:
                    return Response({'error': 'Invalid token'})

            # ORM method tries to extract an object from the database based on the provided parameters, returns a tuple (object, bool)
            user, _ = Users.objects.get_or_create(
                # phone=decoded_token["phoneNumber"],
                esiaId=decoded_token["esiaId"],
                defaults={"name": decoded_token["firstName"] + ' ' + decoded_token["lastName"]}
            )
            # user.generate_token()
            login(request, user)

            if bind_url is not None and bind_url.strip() != '':
                bind_url_decoded = base64.b64decode(bind_url.encode('utf-8')).decode('utf-8')
                a = user.auth_token
                return HttpResponseRedirect(redirect_to=f'{bind_url_decoded}&authCode={user.auth_token}')

            # return Response({'auth_token': user.auth_token}, status=status.HTTP_200_OK)
            return HttpResponseRedirect(redirect_to='/devices')

