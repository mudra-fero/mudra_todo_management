from rest_framework import viewsets, permissions
from .models import User
from lib.pagination import CustomUserPagination
from .permissions import IsAdmin, IsAdminOrManager
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomUserPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        if self.action == 'update':
            return UserSerializer
        elif self.action == 'create':
            return RegisterSerializer
        return False

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'delete']:
            return [IsAdmin()]
        elif self.action == 'update':
            return [IsAdminOrManager()]
        elif self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
