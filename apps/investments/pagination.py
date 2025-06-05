from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class InvestmentPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        response = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "results": data
        }

        if self.page.number > 1:
            response["previous"] = self.get_previous_link()

        return Response(response)
