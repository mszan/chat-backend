from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import Room, RoomInviteKey, CustomUser, Message
from .permissions import IsRoomAdminOrStaff, ActionBasedPermission, IsInviteKeyCreatorOrRoomAdminOrStaff, RejectAll
from .serializers import CustomUserSerializer, RoomSerializer, RoomInviteKeySerializer, MessageSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying User objects.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        permissions.AllowAny: ['list'],
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

    def list(self, request, *args, **kwargs):
        """
        Overrides list view.
        If user is NOT staff, it displays all invite key objects user created.
        If user is staff, it displays all invite key objects.
        """
        queryset = self.queryset
        if not request.user.is_staff:
            queryset = RoomInviteKey.objects.filter(
                Q(creator=self.request.user) | Q(room__admins__in=[self.request.user])
            )
        serializer_context = {'request': request}
        serializer = RoomInviteKeySerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)


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
