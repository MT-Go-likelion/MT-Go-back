from rest_framework.pagination import PageNumberPagination

class lodingListPagination(PageNumberPagination):
    page_size = 8  
class recreationListPagination(PageNumberPagination):
    page_size = 8
class reviewListPagination(PageNumberPagination):
    page_size = 4
