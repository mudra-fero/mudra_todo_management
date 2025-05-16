from collections import Counter

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomUserPagination(LimitOffsetPagination):
    page_size = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_page_size = 1000

    def get_paginated_response(self, data):
        role_counts = Counter(user["role"] for user in data)
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
