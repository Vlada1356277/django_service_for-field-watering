from rest_framework.authentication import TokenAuthentication
from rest_framework import authentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    # authentication.TokenAuthentication.keyword = 'Bearer'
