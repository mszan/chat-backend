from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from chat.models import Room


class UserLoginForm(AuthenticationForm):
    """
    Form used to login registered users.
    """

    class Meta:
        model = User
        fields = ['username', 'password']


class RoomCreateForm(forms.Form):
    """
    Form used to create a new room.
    """
    room_name = forms.CharField(max_length=50, required=True)       # Room name.

    class Meta:
        model = Room
        fields = ['room_name']

    def __init__(self, *args, **kwargs):
        super(RoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['room_name'].help_text = "Max 50 characters."   # Help text for 'room_name' field.
