from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import UserProfile
from .pagination import CustomUserPagination
from .permissions import IsAdmin, IsAdminOrManager
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomUserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "user__email"]

    def get_queryset(self):
        queryset = UserProfile.objects.select_related("user").all()

        roles = self.request.query_params.getlist("filter[]")
        if roles:
            roles = [role.upper() for role in roles]
            queryset = queryset.filter(role__in=roles)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "update"]:
            return UserSerializer
        elif self.action == "create":
            return RegisterSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "destroy"]:
            return [IsAdmin()]
        elif self.action == "update":
            return [IsAdminOrManager()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
            profile.user.delete()
            profile.delete()
            return Response(
                {"detail": "User and profile deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["patch"],
        url_path="change-password",
        permission_classes=[IsAdmin],
    )
    def change_password(self, request, pk=None):
        try:
            profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": profile.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["post"]


class CurrentUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ["get"]
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
