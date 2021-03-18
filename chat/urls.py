from django.urls import path

from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('lobby/', views.LobbyView.as_view(), name='lobby'),
    path('room/<str:room_name>/', views.RoomView.as_view(), name='room'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
