from rest_framework import pagination
from rest_framework.response import Response


class TotalPagePagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'currentPage': self.page.number,
            'count': self.page.paginator.count,
            'totalPage': self.page.paginator.num_pages,
            'results': data
        })
