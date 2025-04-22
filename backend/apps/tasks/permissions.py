from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin"

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["Admin", "Manager"]

class IsAssignedOrPrivileged(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by or
            request.user in obj.assigned_to.all() or
            request.user in obj.collaborators.all()
        )
