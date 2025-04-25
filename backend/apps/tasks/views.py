from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tasks.pagination import CustomUserPagination
from .filters import TaskFilter
from .models import Task, Comment
from .serializers import (
    CreateTaskSerializer,
    TaskSerializer,
    AssignTaskSerializer,
    CollaboratorTaskSerializer,
    CommentSerializer,
    TaskHistorySerializer,
)
from .permissions import IsManagerOrAdmin, IsAssignedOrPrivileged


class TaskViewSet(viewsets.ModelViewSet):
    pagination_class = CustomUserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    serializer_classes = {
        "get": TaskSerializer,
        "post": CreateTaskSerializer,
        "put": CreateTaskSerializer,
        "patch": CreateTaskSerializer,
        "delete": TaskSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method.lower(), TaskSerializer)

    def get_queryset(self):
        user = self.request.user
        if not IsManagerOrAdmin().has_permission(self.request, self):
            return Task.objects.filter(
                Q(assigned_to=user) | Q(collaborators=user)
            ).distinct()
        return Task.objects.all()

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
        print("data = ", request.data)
        task = self.get_object()
        serializer = AssignTaskSerializer(
            data=request.data, context={"task": task, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Task assigned successfully."}, status=status.HTTP_200_OK
        )

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
            comments = Comment.objects.filter(task=task)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CommentSerializer(
                data=request.data, context={"task": task, "request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        task = self.get_object()
        history_entries = task.task_history.all().order_by("-id")
        serializer = TaskHistorySerializer(history_entries, many=True)
        return Response(serializer.data)
