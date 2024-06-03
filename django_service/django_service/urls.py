from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi

from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenVerifyView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from authorize.views import Login, AuthToken
from bonds.views import BondsAPIView, BindDeviceView

#
# from .authorize.views import AuthToken, Login
# from .bonds.views import *


# from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Django service API",
        default_version='v1',
        description="the service to manage users, devices and their bonds",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

router = routers.SimpleRouter()
router.register(r'devices', BondsAPIView, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
    path('devices/bind', BindDeviceView.as_view(), name='devices scan'),
    path('devices/add', BondsAPIView.as_view({'get': 'add_device'}), name='add_device'),
    path('login/', Login.as_view(), name='login'),
    path('send-code/', AuthToken.as_view(), name='send-code'),

    path('admin/', admin.site.urls),
    # path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
