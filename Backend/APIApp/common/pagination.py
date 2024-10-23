from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from APIApp.models import *

# ------ Getting PAGINATION count form ADMINCONFIG  ---------


class ProductPageSizePagination(PageNumberPagination):
    def __init__(self,count):
        pagination_count=count
        self.page_size=pagination_count
        self.page_size_query_param ="page_size"
        self.max_page_size = 10000
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page':self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
            
        })