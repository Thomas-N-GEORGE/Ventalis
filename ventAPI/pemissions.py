"""Custom permission module."""

from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    """Permission class for employee."""

    def has_permission(self, request, view):
        """Check for EMPLOYEE role only."""

        if request.user.role is not "EMPLOYEE":
            return False
        
        return True