from django.urls import path
from apps.users.views import UserViewSet, LoginViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/users/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('api/users/', UserViewSet.as_view({'get': 'list'}), name='users'),
    path('api/users/<int:pk>/', UserViewSet.as_view({'put': 'update', 'delete':'destroy', 'get':'retrieve'}), name='users'),
    path('api/users/login/', LoginViewSet.as_view({'post':'create'}), name='user-login'),
]
