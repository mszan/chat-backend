from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    """
    Room model that holds associated messages and users.
    """
    name = models.TextField(unique=True)
    active = models.BooleanField(default=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_admins')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_users')

    def __str__(self):
        return f'Room {self.name}'


class Message(models.Model):
    """
    Message model related to Room model.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)

    def __str__(self):
        return f'Message {self.id}'
