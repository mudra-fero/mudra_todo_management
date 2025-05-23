from rest_framework import routers
from apps.tasks.views import TaskViewSet, NotificationViewSet

task_router = routers.DefaultRouter()
task_router.register("tasks", TaskViewSet, basename="task")
task_router.register("notifications", NotificationViewSet, basename="notifications")
urlpatterns = task_router.urls
