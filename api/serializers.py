from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Room


class UserSerializer(serializers.HyperlinkedModelSerializer):
    room_admins = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())
    room_users = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'room_admins', 'room_users']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    admins = UserSerializer(many=True, required=False)
    users = UserSerializer(many=True, required=False)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Room
        fields = ['id', 'url', 'name', 'active', 'creator', 'admins', 'users']
