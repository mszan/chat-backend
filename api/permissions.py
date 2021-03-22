from rest_framework import permissions


class IsRoomAdminOrStaff(permissions.IsAuthenticated):
    """
    Custom permission to allow only room admins to edit them.
    """

    def has_object_permission(self, request, view, obj):
        # If user is staff, allow.
        if request.user.is_staff:
            return True

        # Check if user is room admin and if so, allow.
        return request.user in obj.admins.all()
