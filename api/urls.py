from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'rooms-invite-keys', views.RoomInviteKeyViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    re_path('^rooms-join/(?P<invite_key>.+)/$', views.JoinRoomView.as_view()),
]
