from django.urls import path
from rest_framework import routers

from apps.users.views import UserViewSet, LoginViewSet

user_router = routers.SimpleRouter()
user_router.register(r"users", UserViewSet, basename="user")
user_router.register(r"login", LoginViewSet, basename="login")
urlpatterns = user_router.urls
