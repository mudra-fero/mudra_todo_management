from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tasks.pagination import CustomUserPagination, CustomNotificationPagination
from .base import BaseViewSet
from .filters import TaskFilter
from .models import Task, Comment, Notification
from .serializers import (
    CreateTaskSerializer,
    TaskSerializer,
    AssignTaskSerializer,
    CollaboratorTaskSerializer,
    CommentSerializer,
    TaskHistorySerializer,
    NotificationSerializer,
)
from .permissions import IsManagerOrAdmin, IsAssignedOrPrivileged


class TaskViewSet(BaseViewSet):
    pagination_class = CustomUserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    queryset = Task.objects.all()

    dynamic_serializers = {
        "list": TaskSerializer,
        "retrieve": TaskSerializer,
        "create": CreateTaskSerializer,
        "update": CreateTaskSerializer,
        "partial_update": CreateTaskSerializer,
        "destroy": TaskSerializer,
    }

    def get_queryset(self):
        user_profile = self.request.user.profile
        base_queryset = Task.objects.all()

        if not IsManagerOrAdmin().has_permission(self.request, self):
            base_queryset = base_queryset.filter(
                Q(assigned_to=user_profile) | Q(task_collaborations__user=user_profile)
            ).distinct()

        return base_queryset

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "assign",
            "collaborators",
        ]:
            return [IsAuthenticated(), IsManagerOrAdmin()]
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsAssignedOrPrivileged()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        task = self.get_object()
        serializer = AssignTaskSerializer(
            data=request.data, context={"task": task, "request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Task assigned successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def collaborators(self, request, pk=None):
        task = self.get_object()
        serializer = CollaboratorTaskSerializer(
            data=request.data, context={"task": task, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Task collaborated successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        task = self.get_object()

        if request.method == "GET":
            comments = Comment.objects.filter(task=task).order_by("id")
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CommentSerializer(
                data=request.data, context={"task": task, "request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="comments/(?P<comment_id>[^/.]+)")
    def delete_comment(self, request, pk=None, comment_id=None):
        task = self.get_object()

        try:
            comment = Comment.objects.get(id=comment_id, task=task)
        except Comment.DoesNotExist:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        comment.delete()
        task.add_history(
            task=task,
            user=request.user.profile,
            message=f"deleted comment of task {task.title} by {request.user.username}",
        )
        task.add_notification(
            task=task,
            acting_user=request.user.profile,
            message=f"deleted comment of task {task.title} by {request.user.username}",
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        task = self.get_object()
        history_entries = task.task_history.all().order_by("id")
        serializer = TaskHistorySerializer(history_entries, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    pagination_class = CustomNotificationPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        print(self.action)
        user_profile = self.request.user.profile
        if self.action == "list":
            return Notification.objects.filter(user=user_profile).order_by("-id")
        return Notification.objects.all()

    @action(detail=False, methods=["post"], url_path="mark-as-read")
    def mark_as_read(self, request):
        user_profile = request.user.profile
        Notification.objects.filter(user=user_profile, is_read=False).update(
            is_read=True
        )
        return Response(
            {"detail": "All notifications marked as read."}, status=status.HTTP_200_OK
        )
