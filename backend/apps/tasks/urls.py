from rest_framework import routers
from apps.tasks.views import TaskViewSet

task_router = routers.DefaultRouter()
task_router.register("tasks", TaskViewSet, basename="task")
urlpatterns = task_router.urls
