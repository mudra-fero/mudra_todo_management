from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lib.pagination import CustomUserPagination
from .filters import TaskFilter
from .models import Task
from .serializers import (
    CreateTaskSerializer,
    TaskSerializer,
    AssignTaskSerializer,
    CollaboratorTaskSerializer,
)
from .permissions import IsManagerOrAdmin, IsAssignedOrPrivileged


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
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

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsManagerOrAdmin],
    )
    def assign(self, request, pk=None):
        task = self.get_object()
        serializer = AssignTaskSerializer(data=request.data, context={"task": task})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Task assigned successfully."}, status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsManagerOrAdmin],
    )
    def collaborators(self, request, pk=None):
        task = self.get_object()
        serializer = CollaboratorTaskSerializer(
            data=request.data, context={"task": task}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Collaborators updated successfully."}, status=status.HTTP_200_OK
        )
