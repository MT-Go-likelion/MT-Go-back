from django.urls import path
from .views import shoppingMainView, createShoppingView

urlpatterns = [
    path('main/', shoppingMainView.as_view(), name='shoppingMain'),
    path('create/', createShoppingView.as_view(), name='createShopping'),
]