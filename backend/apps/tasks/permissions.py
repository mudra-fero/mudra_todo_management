from rest_framework.permissions import BasePermission
from lib.enum import Roles


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [Roles.ADMIN, Roles.MANAGER]


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.MANAGER


class IsAssignedOrPrivileged(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by
            or request.user in obj.assigned_to.all()
            or request.user in obj.collaborators.all()
        )
