from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'room-invite-keys', views.RoomInviteKeyViewSet)

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
