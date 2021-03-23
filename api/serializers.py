from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Room


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'room_admins', 'room_users']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    admins = UserSerializer(many=True, required=False)
    users = UserSerializer(many=True, required=False)
    creator = serializers.HyperlinkedRelatedField(
        allow_null=True,
        required=False,
        view_name='user-detail',
        read_only=True
    )
    active = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = Room
        fields = ['url', 'name', 'active', 'creator', 'admins', 'users']

    def create(self, validated_data):
        request_user = self.context['request'].user  # Get request user object.
        obj = Room.objects.create(**validated_data)  # Create new Room object with validated data.
        obj.admins.add(request_user)  # Add request user to admins.
        obj.users.add(request_user)  # Add request user to users.
        obj.creator = request_user  # Add request user to creator.
        obj.save()  # Save instance.
        return obj
