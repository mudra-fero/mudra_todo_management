from django.urls import path

from apps.tasks.views import TaskViewSet

urlpatterns = [
    path(
        "api/tasks/<int:pk>/assign/",
        TaskViewSet.as_view({"post": "assign"}),
        name="assign-tasks",
    ),
    path(
        "api/tasks/<int:pk>/collaborate/",
        TaskViewSet.as_view({"post": "collaborators", "delete": "collaborators"}),
        name="collaborate-tasks",
    ),
    path(
        "api/tasks/",
        TaskViewSet.as_view({"post": "create", "get": "list"}),
        name="tasks",
    ),
    path(
        "api/tasks/<int:pk>/",
        TaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="tasks",
    ),
]
