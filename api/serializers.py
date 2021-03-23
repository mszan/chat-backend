from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Room


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'room_admins', 'room_users']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    active = serializers.BooleanField(required=False)
    creator = serializers.HyperlinkedRelatedField(
        allow_null=True,
        required=False,
        view_name='user-detail',
        read_only=True
    )

    class Meta:
        model = Room
        fields = ['url', 'name', 'active', 'creator', 'admins', 'users']

    def create(self, validated_data):
        """
        Overrides creation of new object.
        Sets fields such as room_admins, room_users, creator.
        """
        room_admins = validated_data.pop('admins')    # Pop due to *-* assignment.
        room_users = validated_data.pop('users')      # Pop due to *-* assignment.

        obj = Room.objects.create(**validated_data)   # Create new object with validated data.
        obj.admins.set(room_admins)                   # Add request user to admins.
        obj.users.set(room_users)                     # Add request user to users.

        request_user = self.context['request'].user   # Get request user object.
        obj.creator = request_user                    # Add request user to creator.
        obj.save()                                    # Save instance.
        return obj
