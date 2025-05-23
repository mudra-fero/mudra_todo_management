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
        user_profile = getattr(request.user, "profile", None)
        if not user_profile:
            return False

        is_creator = obj.created_by == user_profile
        is_assigned = obj.assigned_to == user_profile if obj.assigned_to else False
        is_collaborator = obj.task_collaborations.filter(user=user_profile).exists()

        return is_creator or is_assigned or is_collaborator


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff
