from rest_framework.pagination import PageNumberPagination


class HotelPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class RoomPagination(PageNumberPagination):
    page_size = 8