from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'room-invite-keys', views.RoomInviteKeyViewSet)

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),
]
