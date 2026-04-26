from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Custom permission, which check user group has Moderator"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()
