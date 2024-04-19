from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi

from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenVerifyView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from bonds.views import *
from auth.views import AuthToken, LoginPageView, AuthCode

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
router.register(r'devices', BondsAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('devices/bind', BindDeviceView.as_view()),
    # path('devices/', BondsAPIView.as_view()),
    # path('devices/<int:pk>/', BondsUpdate.as_view()),
    path('login/', LoginPageView.as_view()),
    path('login/', LoginPageView.as_view()),
    path('auth-send-code/', AuthCode.as_view()),
    path('auth-get-token/', AuthToken.as_view()),

    path('admin/', admin.site.urls),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
