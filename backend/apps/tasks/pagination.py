from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from apps.tasks.models import Notification


class CustomUserPagination(LimitOffsetPagination):
    page_size = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.count,
                "results": data,
            }
        )


class CustomNotificationPagination(LimitOffsetPagination):
    page_size = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_page_size = 1000

    def get_paginated_response(self, data):
        user = self.request.user
        unread_count = 0
        if user:
            unread_count = Notification.objects.filter(
                user=user.profile, is_read=False
            ).count()
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.count,
                "unread_count": unread_count,
                "results": data,
            }
        )
