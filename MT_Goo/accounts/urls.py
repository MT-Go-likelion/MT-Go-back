from django.urls import path
from .views import UserCreateView, UserRetrieveUpdateDestroyView, LoginView, LogoutView

urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/login/', LoginView.as_view(), name='user-login'),
    path('user/logout/', LogoutView.as_view(), name='user-logout'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]
