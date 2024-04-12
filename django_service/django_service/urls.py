from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Django service API",
#         default_version='v1',
#         description="the service to manage users, devices and their bonds",
#     ),
#     public=True,
#     # permission_classes=[permissions.AllowAny,],
# )

from bonds.views import BondsAPIView

urlpatterns = [
    path('devices/', BondsAPIView.as_view()),
    path('admin/', admin.site.urls),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger')
]
