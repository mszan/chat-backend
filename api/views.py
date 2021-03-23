from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from chat.models import Room
from .permissions import IsRoomAdminOrStaff, ActionBasedPermission
from .serializers import UserSerializer, RoomSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying User objects.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


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
        Overrides list view.
        If user is staff, it returns all Room objects.
        If user is NOT staff, it returns all Room objects user has admin in.
        """
        if request.user.is_staff:
            queryset = Room.objects.all()
        else:
            queryset = Room.objects.filter(admins__in=[self.request.user])

        serializer_context = {'request': request}   # HyperlinkedIdentityField requires serializer context to be passed.
        serializer = RoomSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)
