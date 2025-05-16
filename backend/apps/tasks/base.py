from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.tasks.constant import HttpMethods


class BaseViewSet(ModelViewSet):
    dynamic_serializers = {}
    filter_backends = [SearchFilter]
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
