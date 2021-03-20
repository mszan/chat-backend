from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    # Django rest framework.
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
