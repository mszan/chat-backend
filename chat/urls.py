from django.urls import path

from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('lobby/', views.LobbyView.as_view(), name='lobby'),
    path('room/create/', views.RoomCreateView.as_view(), name='room-create'),
    path('room/<str:room_name>/', views.RoomView.as_view(), name='room'),
    path('room/join/<str:invitation_key>/', views.RoomJoinFromInvitationView.as_view(), name='room-join-from-invitation'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
