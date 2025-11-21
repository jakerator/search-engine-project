"""
URL configuration for app project.

"""
from django.contrib import admin
from django.urls import path, include

from api.views import api_root


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
