from django.urls import path
from rest_framework import routers

from apps.tasks.views import TaskViewSet


task_router = routers.SimpleRouter()
task_router.register(r"tasks", TaskViewSet, basename="task")
urlpatterns = task_router.urls
