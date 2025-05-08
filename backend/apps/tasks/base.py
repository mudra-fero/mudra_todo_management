from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.tasks.constant import HttpMethods


class BaseViewSet(ModelViewSet):
    filterset_class = None
    dynamic_serializers = {}
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    http_method_names = [
        HttpMethods.GET,
        HttpMethods.POST,
        HttpMethods.PUT,
        HttpMethods.PATCH,
        HttpMethods.DELETE,
    ]

    def get_serializer_class(self):
        serializer_dict = self.dynamic_serializers
        if not serializer_dict:
            return self.serializer_class
        return serializer_dict[self.action]
