from collections import Counter

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomUserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 1000

    def get_paginated_response(self, data):
        role_counts = Counter(user["role"] for user in data)
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "role_counts": role_counts,
                "results": data,
            }
        )
