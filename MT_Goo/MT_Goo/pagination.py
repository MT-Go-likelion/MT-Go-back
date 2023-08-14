from rest_framework.pagination import PageNumberPagination

class lodingListPagination(PageNumberPagination):
    page_size = 1  
class recreationListPagination(PageNumberPagination):
    page_size = 4
class reviewListPagination(PageNumberPagination):
    page_size = 4
