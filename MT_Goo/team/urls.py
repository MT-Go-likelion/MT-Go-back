from django.urls import path
from .views import teamSpaceView, teamSpaceLodgingView, teamSpaceRecreationView, teamSpaceShoppingView

urlpatterns = [
    path('teamSpace/', teamSpaceView.as_view(), name='teamSpace'),
    path('teamSpaceLodging/', teamSpaceLodgingView.as_view(), name='teamSpaceLodging'),
    path('teamSpaceRecreation/', teamSpaceRecreationView.as_view(), name='teamSpaceRecreation'),
    path('teamSpaceShopping/', teamSpaceShoppingView.as_view(), name='teamSpaceShopping'),
]