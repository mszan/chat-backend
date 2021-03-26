from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView

from chat.forms import UserLoginForm, RoomCreateForm
from chat.models import Message, Room, RoomInviteKey


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

    # If user is already logged in.
    if request.user.is_authenticated:
        redirect('lobby')

    # Login user.
    if request.method == 'POST':
        # Get passed login form.
        form = UserLoginForm(request, data=request.POST)

        # If passed form is valid.
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Get username from passed form.
            password = form.cleaned_data.get('password')  # Get password from passed form.
            user = authenticate(request, username=username, password=password)  # Try to authenticate user.

            # If user has been authenticated.
            if user is not None:
                login(request, user)  # Login user on success.
                messages.success(request, 'Logged in successfully.')
                return redirect('lobby')  # Redirect to lobby.
            else:
                messages.warning(request, 'You need to login first.')
        else:
            messages.warning(request, 'Something went wrong, try again.')

    # Display login form.
    else:
        # If user has been redirected from login-required view.
        if request.GET.get('next') is not None:
            messages.warning(request, 'You need to login first.')

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

    def get(self, request, *args, **kwargs):
        # If user is not authenticated.
        if not request.user.is_authenticated:
            messages.warning(request, 'You need to login first.')
            return redirect('login')  # Redirect to login page.

        room_name = self.kwargs['room_name']  # Chat room name.

        # If room object exists in database.
        if Room.objects.filter(name=room_name).exists():
            room_object = Room.objects.get(name=room_name)  # Room object instance.

            # If user is allowed to join the room.
            if request.user not in room_object.users.all():
                # If user is not allowed, display a message and redirect to lobby.
                messages.warning(request, f'You do not have access to room <strong>{room_name}</strong>.')
                return redirect('lobby')
        # If room doesn't exist.
        else:
            # Redirect to room creation view.
            messages.warning(request, f'The room does not exist.')
            return redirect('room-create')

        # Parse last (previous) messages from database and serialize them.
        last_messages = serializers.serialize(
            "json",
            Message.objects.filter(room=room_object),
            use_natural_foreign_keys=True
        )

        # Render template.
        return render(request, 'chat/room.html', {
            'last_messages': last_messages,
            'room_object': room_object
        })


class RoomCreateView(LoginRequiredMixin, DetailView):
    """
    Displays a confirmation page where user can confirm he wants
    to create a new room. Redirects to newly created room afterwards.
    """
    # model = Room
    login_url = '/login'
    model = Room

    def get(self, request, *args, **kwargs):
        """
        Render room creation form and pass its data to POST.
        """
        room_create_form = RoomCreateForm()   # Create form instance.
        return render(request, 'chat/room_create.html', {'room_create_form': room_create_form})

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Create room object and redirect to room page.
        """

        room_name = request.POST['room_name']                           # Get room name.
        if not Room.objects.filter(name=room_name):                     # Check if room object does not exist.
            room_object = Room(name=room_name, creator=request.user)    # Create new room object.
            room_object.save()                                          # Save created object to database.
            room_object.users.add(request.user)                         # Add user to room users field.
            room_object.admins.add(request.user)                        # Add creator to room admins field.
            return redirect('room', room_name=room_name)                # Redirect to newly created room.
        else:
            messages.warning(request, f'Room {room_name} already exists. Please choose other room name.')
            return redirect('room-create')


class RoomJoinFromInviteView(LoginRequiredMixin, DetailView):
    """
    Handles joining to room from key invites.
    Redirects to specific room if invite key is valid.
    """
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        # If invite key parameter is passed.
        invite_key = self.kwargs['invite_key']
        if not invite_key:
            # If not, redirect to lobby with a message.
            messages.warning(request, 'Key is missing.')
            return redirect('lobby')

        # If key object exists in database.
        key_object = RoomInviteKey.objects.filter(key=invite_key).first()
        if not key_object:
            # If not, redirect to lobby with a message.
            messages.warning(request, 'Key is invalid.')
            return redirect('lobby')

        # If key date is valid (hasn't expired).
        if key_object.valid_due.date() < date.today():
            # If not, redirect to lobby with a message.
            messages.warning(request, 'Key has expired.')
            return redirect('lobby')

        # If room this key was made for exists.
        room_name = key_object.room.name
        if not room_name:
            # If not, redirect to lobby with a message.
            messages.warning(request, 'Room this key was made for does not exist.')
            return redirect('lobby')

        # If invite key was created only for specific user.
        if key_object.only_for_this_user:
            # If currently authenticated user matches with invite's 'only_for_this_user' field.
            if key_object.only_for_this_user == request.user:
                key_object.room.users.add(request.user)  # Add user to room.
                key_object.delete()  # Delete invite key.
            else:
                messages.warning(request, 'Key is not yours.')
                return redirect('lobby')
        # If invite key was created for anyone.
        else:
            key_object.room.users.add(request.user)  # Add user to room.

        return redirect('room', room_name=room_name)
