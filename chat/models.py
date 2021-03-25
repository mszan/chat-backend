from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Room(models.Model):
    """
    Room model that holds associated messages and users.
    """
    name = models.TextField(max_length=50, unique=True)  # Room name.
    active = models.BooleanField(default=True)  # Allow users to join the room.
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    admins = models.ManyToManyField(  # Administrator users.
        settings.AUTH_USER_MODEL,
        default=None,
        related_name='room_admins'
    )
    users = models.ManyToManyField(  # Normal users.
        settings.AUTH_USER_MODEL,
        default=None,
        related_name='room_users'
    )

    def __str__(self):
        return f'Room | name:{self.name}'


class Message(models.Model):
    """
    Message model that holds user messages.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)  # Room the message is in.
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # User that sent the message.
    timestamp = models.DateTimeField(auto_now_add=True)  # Time message was sent.
    text = models.TextField(null=False)  # Message text content.

    def __str__(self):
        return f'Message | id:{self.id}'


def get_inivitation_key_expire_date():
    """
    :returns: Invitation key expire date.
    """
    return timezone.now() + timezone.timedelta(hours=2)  # Valid for 2 hours.


class InvitationKey(models.Model):
    """
    Invitation key model that holds access keys for rooms.
    """
    key = models.TextField(null=False, unique=True)  # Invitation key itself.
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)  # Room the key is used with.
    only_for_this_user = models.ForeignKey(  # Only for specific user.
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True
    )
    valid_due = models.DateTimeField(default=get_inivitation_key_expire_date)  # Valid until.
    give_admin = models.BooleanField(default=False)  # Give admin to this user.

    def __str__(self):
        return f'Key | id:{self.id}, key:{self.key}'
