from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserModelViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', UserModelViewSet, basename='user')

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls))
]
