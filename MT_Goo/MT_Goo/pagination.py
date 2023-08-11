from rest_framework.pagination import PageNumberPagination

class lodingListPagination(PageNumberPagination):
    page_size = 1  
class recreationListPagination(PageNumberPagination):
    page_size = 1  
class reviewListPagination(PageNumberPagination):
    page_size = 1
