from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, routers

from authorize.views import Login, AuthToken
from bonds.views import BondsAPIView, BindDeviceView
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Django service API",
        default_version='v1',
        description="The service to manage users, devices, and their bonds",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()
router.register(r'devices', BondsAPIView, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
    path('devices/bind', BindDeviceView.as_view(), name='devices scan'),
    path('devices/add', BondsAPIView.as_view({'get': 'add_device'}), name='add_device'),
    path('login/', Login.as_view(), name='login'),
    path('send-code/', AuthToken.as_view(), name='send-code'),
    path('device/<str:device_sn>/', DeviceDetailsView.as_view(), name='get logger devices'),

    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]