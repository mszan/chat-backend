from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Room


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'url', 'name', 'active', 'admins', 'users']
