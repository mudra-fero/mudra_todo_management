from rest_framework import routers
from apps.users.views import (
    UserViewSet,
    LoginViewSet,
    CurrentUserViewSet,
    ListAllUserViewSet,
)

user_router = routers.DefaultRouter()
user_router.register("users", UserViewSet, basename="user")
user_router.register("all/users", ListAllUserViewSet, basename="users")
user_router.register("current/user", CurrentUserViewSet, basename="current_user")
user_router.register("login", LoginViewSet, basename="login")
urlpatterns = user_router.urls
