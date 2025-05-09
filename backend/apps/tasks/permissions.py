from rest_framework.permissions import BasePermission
from lib.enum import Roles


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role in [Roles.ADMIN, Roles.MANAGER]


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == Roles.MANAGER


class IsAssignedOrPrivileged(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by
            or request.user.profile in obj.assigned_to.all()
            or request.user.profile in obj.collaborators.all()
        )


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff
