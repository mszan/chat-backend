from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from chat.models import Room, RoomInviteKey


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer associated with built-in User model.
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'room_admins', 'room_users']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer associated with Room model.
    """
    active = serializers.BooleanField(
        required=False
    )
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


class RoomInviteKeySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer associated with RoomInviteKey model.
    """
    key = serializers.CharField(
        validators=[UniqueValidator(queryset=RoomInviteKey.objects.all())],
        read_only=True
    )
    creator = serializers.HyperlinkedRelatedField(
        allow_null=True,
        required=False,
        view_name='user-detail',
        read_only=True
    )
    room = serializers.HyperlinkedRelatedField(
        queryset=Room.objects.none(),
        required=False,
        view_name='room-detail'
    )
    valid_due = serializers.DateTimeField(
        required=False,
        read_only=True
    )

    class Meta:
        model = RoomInviteKey
        fields = ['url', 'id', 'key', 'creator', 'room', 'only_for_this_user', 'valid_due', 'give_admin']

    def get_fields(self):
        """
        Overrides queryset for 'room' field.
        """
        fields = super(RoomInviteKeySerializer, self).get_fields()

        # If user is admin, return all Room objects.
        if self.context['request'].user.is_staff:
            fields['room'].queryset = Room.objects.all()
        # Else, return Room objects request user is admin in.
        else:
            fields['room'].queryset = Room.objects.filter(admins__in=[self.context['request'].user])
        return fields

    def create(self, validated_data):
        """
        Overrides creation of new object.
        Sets creator field.
        """
        request_user = self.context['request'].user           # Get request user object.
        obj = RoomInviteKey.objects.create(**validated_data)  # Create new object with validated data.
        obj.creator = request_user                            # Add request user to creator field.
        obj.save()                                            # Save instance.
        return obj
