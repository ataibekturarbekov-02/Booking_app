from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserProfileListAPIView, UserProfileDetailAPIView,
                    CityListAPIView, CityDetailAPIView,
                    ServiceViewSet, RegisterViewSet, LoginViewSet, LogoutViewSet,
                    RoomListAPIView, RoomDetailAPIView, RoomImageViewSet,
                    HotelListAPIView, HotelDetailAPIView,
                    BookingViewSet, ReviewViewSet)


router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'room_images', RoomImageViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('room/', RoomListAPIView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room_detail'),
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('logout/', LogoutViewSet.as_view(), name='logout')
]