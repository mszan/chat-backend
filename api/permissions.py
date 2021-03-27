from rest_framework import permissions
from rest_framework.permissions import AllowAny


class RejectAll(permissions.BasePermission):
    """
    Reject access.
    """
    def has_permission(self, request, view):
        return False


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a request
    type mapping in view.action_permissions.
    """
    def has_permission(self, request, view):
        for cls, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return cls().has_permission(request, view)
        return False


class IsRoomAdminOrStaff(permissions.IsAuthenticated):
    """
    Custom permission to allow only room admins to access them.
    """

    def has_object_permission(self, request, view, obj):
        # If user is staff, allow.
        if request.user.is_staff:
            return True

        # Check if user is room admin and if so, allow.
        return request.user in obj.admins.all()


class IsInviteKeyCreatorOrRoomAdminOrStaff(permissions.IsAuthenticated):
    """
    Custom permission to allow only invite key creators
    or invite key's room administrators to access them.
    """

    def has_object_permission(self, request, view, obj):
        # If user is staff, allow.
        if request.user.is_staff:
            return True

        # Check if user is room admin and if so, allow.
        if request.user in obj.room.admins.all():
            return True

        # Check if user is key creator and if so, allow.
        return request.user in obj.room.creator