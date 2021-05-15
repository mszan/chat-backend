from django.db.models import Q
from rest_framework import viewsets, permissions, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Room, RoomInviteKey, CustomUser, Message
from .permissions import IsRoomAdminOrStaff, ActionBasedPermission, IsInviteKeyCreatorOrRoomAdminOrStaff, RejectAll
from .serializers import CustomUserSerializer, RoomSerializer, RoomInviteKeySerializer, MessageSerializer

from django.utils import timezone
import pytz


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for displaying and creating User objects.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        permissions.AllowAny: ['list', 'create'],
        permissions.IsAdminUser: ['retrieve']
    }
    lookup_field = 'username'

    def list(self, request, *args, **kwargs):
        """
        Overrides list view.
        If user is staff, display all users.
        If user is NOT staff, display only logged user.
        """
        if request.user.is_staff:
            queryset = CustomUser.objects.all()
        else:
            queryset = CustomUser.objects.filter(username=self.request.user)

        serializer_context = {'request': request}
        serializer = CustomUserSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """
    View for displaying, creating and updating Room objects.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        permissions.IsAdminUser: ['destroy'],
        permissions.IsAuthenticated: ['create', 'list'],
        IsRoomAdminOrStaff: ['update', 'partial_update', 'retrieve']
    }

    def list(self, request, *args, **kwargs):
        """
        Overrides list view to display rooms this user
        participate in (user is in Room's 'users' field).
        """
        queryset = Room.objects.filter(users__in=[self.request.user])

        # Check for optional parameter 'active'.
        only_active = self.request.query_params.get('active')
        if only_active is not None:
            # If its value equals 'true', filter only for active rooms.
            if only_active.lower() == 'true':
                queryset = queryset.filter(active=True)

        serializer_context = {'request': request}
        serializer = RoomSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


class RoomInviteKeyViewSet(viewsets.ModelViewSet):
    """
    View for displaying, creating and deleting room invite key objects.
    """
    queryset = RoomInviteKey.objects.all()
    serializer_class = RoomInviteKeySerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        permissions.IsAdminUser: ['destroy'],
        permissions.IsAuthenticated: ['list'],
        IsInviteKeyCreatorOrRoomAdminOrStaff: ['create', 'retrieve'],
        RejectAll: ['update', 'partial_update']
    }

    def get_queryset(self):
        """
        Handle optional request parameters to filter the queryset.
        """
        queryset = RoomInviteKey.objects.all()

        # Optional 'room_id' request parameter handling.
        room_id = self.request.query_params.get('room_id')
        if room_id is not None:
            queryset = queryset.filter(room_id=room_id)

        # Optional 'key' request parameter handling.
        key = self.request.query_params.get('key')
        if key is not None:
            queryset = queryset.filter(key=key)

        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    """
    View for displaying and creating room messages.
    By default, it returns empty queryset. To retrieve messages, parameter 'room_id' must be passed.
    """
    queryset = Message.objects.none()
    serializer_class = MessageSerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        permissions.IsAdminUser: ['destroy'],
        permissions.IsAuthenticated: ['list', 'create', 'retrieve'],
        RejectAll: ['update', 'partial_update']
    }

    def list(self, request, *args, **kwargs):
        """
        Overrides list view to return messages related with room_id parameter.
        """
        room_id = self.request.query_params.get('room_id')

        if room_id:
            queryset = Message.objects.filter(room_id=room_id)
        else:
            return Response("Parameter 'room_id' missing.", status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_context = {'request': request}
        serializer = MessageSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


class JoinRoomView(generics.GenericAPIView):
    """
    View for joining users to room objects.
    """
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        TODO: This may be an invalid request method. Anyway, it works for now.

        Handles invitations and joining users to specific rooms.
        """
        invite_key_str = self.kwargs.get('invite_key')
        response_data = {}

        try:
            invite_key = RoomInviteKey.objects.get(key=invite_key_str, valid_due__gte=timezone.now())
            invite_key_marked_for_deletion = False     # Tells whether to delete invite_key after all the operations.

            # One user only logic
            if invite_key.only_for_this_user and invite_key.only_for_this_user == self.request.user:
                invite_key.room.users.add(self.request.user)
                invite_key_marked_for_deletion = True
            else:
                response_data['msg'] = "Invite key is valid for another user, not for you."
                return Response(data=response_data, status=status.HTTP_403_FORBIDDEN)

            # Give admin logic
            if invite_key.give_admin:
                invite_key.room.admins.add(self.request.user)
                invite_key_marked_for_deletion = True

            response_data['room_id'] = invite_key.room.id

            if invite_key_marked_for_deletion:
                invite_key.delete()

            return Response(data=response_data, status=status.HTTP_200_OK)
        except (RoomInviteKey.DoesNotExist, Room.DoesNotExist):
            response_data['msg'] = "Something went wrong. Make sure invite key is valid and it hasn't expired."
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        