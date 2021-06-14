from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.CustomUserViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'rooms-invite-keys', views.RoomInviteKeyViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts/registration/', include('rest_auth.registration.urls')),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('accounts/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('accounts/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    re_path('^rooms-join/(?P<invite_key>.+)/', views.JoinRoomView.as_view()),
]
