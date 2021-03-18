from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView

from chat.forms import UserLoginForm
from chat.models import Message


class HomeView(TemplateView):
    """
    Landing view.
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'chat/home.html')


class LobbyView(LoginRequiredMixin, DetailView):
    """
    Displays a Lobby.
    """
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'chat/lobby.html')


def login_view(request):
    """
    Logins user on POST, displays login form on GET.
    """

    # Check if user is already logged in.
    if request.user.is_authenticated:
        redirect('lobby')

    # Login user.
    if request.method == 'POST':
        # Get passed login form.
        form = UserLoginForm(request, data=request.POST)

        # Check if passed form is valid.
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Get username from passed form.
            password = form.cleaned_data.get('password')  # Get password from passed form.
            user = authenticate(request, username=username, password=password)  # Try to authenticate user.

            # Check if user has been authenticated.
            if user is not None:
                login(request, user)  # Login user on success.
                messages.success(request, 'Logged in successfully.')  # Display message to user.
                return redirect('lobby')  # Redirect to lobby.
            else:
                messages.warning(request, 'You need to login first.')  # Display message to user.
        else:
            messages.warning(request, 'Something went wrong, try again.')  # Display message to user.

    # Display login form.
    else:
        # Check if user has been redirected from login-required view.
        if request.GET.get('next') is not None:
            messages.warning(request, 'You need to login first.')  # Display message to user.

        # Create empty form to be passed in context.
        form = UserLoginForm()

    # Render template.
    return render(request, 'chat/login_form.html', {'form': form})


def logout_view(request):
    """
    Logouts user.
    """
    logout(request)
    messages.success(request, 'Logged out. Bye bye!')
    return redirect('login')


class RoomView(LoginRequiredMixin, DetailView):
    """
    Displays a chat room.
    """
    login_url = '/login/'
    print('yo')

    def get(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']  # Chat room name.

        #   Check if user is not authenticated.
        if not request.user.is_authenticated:
            messages.warning(request, 'You need to login first.')  # Display message to user.
            redirect('login')  # Redirect to login page.

        # Parse last (previous) messages from database.
        last_messages = serializers.serialize("json", Message.objects.all())

        # Render template.
        return render(request, 'chat/room.html', {
            'last_messages': last_messages,
            'room_name': room_name
        })
