from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import Room, RoomInviteKey, CustomUser, Message


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer associated with built-in User model.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'room_admins', 'room_users']
        lookup_field = 'username'


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer associated with Message model.

    Takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    user = serializers.SlugRelatedField(
        allow_null=True,
        required=False,
        read_only=True,
        slug_field='username'
    )
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.none(),
        required=False,
        # view_name='room-detail'
    )

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'text', 'timestamp']

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(MessageSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_fields(self):
        """
        Overrides queryset for 'room' field.
        """
        fields = super(MessageSerializer, self).get_fields()

        # If user is admin, return all Room objects.
        if self.context['request'].user.is_staff:
            fields['room'].queryset = Room.objects.all()
        # Else, return Room objects request user participate in.
        else:
            fields['room'].queryset = Room.objects.filter(users__in=[self.context['request'].user])
        return fields

    def create(self, validated_data):
        """
        Overrides creation of new object.
        Sets fields such as room and user.
        """
        obj = Message.objects.create(**validated_data)  # Create new object with validated data.
        request_user = self.context['request'].user  # Get request user object.
        obj.user = request_user  # Add request user to creator.
        obj.save()  # Save instance.
        return obj


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer associated with Room model.

    Takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    active = serializers.BooleanField(
        required=False
    )

    creator = serializers.SlugRelatedField(
        allow_null=True,
        required=False,
        slug_field='username',
        read_only=True
    )

    admins = serializers.SlugRelatedField(
        allow_null=True,
        many=True,
        required=False,
        slug_field='username',
        read_only=True
    )

    users = serializers.SlugRelatedField(
        allow_null=True,
        many=True,
        required=False,
        slug_field='username',
        read_only=True
    )

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(RoomSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Room
        fields = ['id', 'url', 'name', 'active', 'creator', 'timestamp', 'admins', 'users']

    def create(self, validated_data):
        """
        Overrides creation of new object.
        Sets fields such as room_admins, room_users, creator.
        """

        # room_admins = validated_data.pop('admins')    # Pop due to *-* assignment.
        # room_users = validated_data.pop('users')      # Pop due to *-* assignment.

        obj = Room.objects.create(**validated_data)   # Create new object with validated data.

        request_user = self.context['request'].user   # Get request user object.
        obj.creator = request_user                    # Add request user to creator.
        obj.admins.set([request_user])                   # Add request user to admins.
        obj.users.set([request_user])                     # Add request user to users.
        obj.save()                                    # Save instance.
        return obj


class RoomInviteKeySerializer(serializers.ModelSerializer):
    """
    Serializer associated with RoomInviteKey model.
    """
    key = serializers.CharField(
        validators=[UniqueValidator(queryset=RoomInviteKey.objects.all())],
        read_only=True
    )
    creator = serializers.SlugRelatedField(
        allow_null=True,
        required=False,
        # view_name='customuser-detail',
        slug_field='username',
        read_only=True
    )
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.none(),
        required=False,
        # view_name='room-detail'
    )
    valid_due = serializers.DateTimeField(
        required=False,
        read_only=True
    )
    only_for_this_user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        allow_null=True,
        required=False,
        slug_field='username',
    )

    class Meta:
        model = RoomInviteKey
        fields = ['id', 'key', 'creator', 'room', 'only_for_this_user', 'valid_due', 'give_admin']

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