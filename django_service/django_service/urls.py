from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, routers
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.schemas import get_schema_view
from authorize.views import Login, AuthToken
from bonds.views import BondsAPIView, BindDeviceView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# schema_view = get_schema_view(
#     title="Django service API",
#     description="The service to manage users, devices, and their bonds",
#     version="1.0.0",
#     renderer_classes=[BrowsableAPIRenderer, JSONRenderer],  # Optional: You can choose different renderers
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

router = routers.SimpleRouter()
router.register(r'devices', BondsAPIView, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
    path('devices/bind', BindDeviceView.as_view(), name='devices scan'),
    path('devices/add', BondsAPIView.as_view({'get': 'add_device'}), name='add_device'),
    path('login/', Login.as_view(), name='login'),
    path('send-code/', AuthToken.as_view(), name='send-code'),

    path('admin/', admin.site.urls),

    # OpenAPI schema endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
    # path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
