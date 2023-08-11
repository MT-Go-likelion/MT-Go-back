from django.urls import path
from .views import teamSpaceView, joinTeamSpaceView, teamUserView, teamSpaceLodgingView, teamSpaceRecreationView, teamSpaceShoppingView, teamSpaceLodgingScrapView, teamSpaceRecreationScrapView

urlpatterns = [
    path('teamSpace/', teamSpaceView.as_view(), name='teamSpace'),
    path('teamSpace/join/', joinTeamSpaceView.as_view(), name='joinTeamSpace'),
    path('teamSpace/users/', teamUserView.as_view(), name='users'),
    path('teamSpaceLodging/', teamSpaceLodgingView.as_view(), name='teamSpaceLodging'),
    path('teamSpaceRecreation/', teamSpaceRecreationView.as_view(), name='teamSpaceRecreation'),
    path('teamSpaceShopping/', teamSpaceShoppingView.as_view(), name='teamSpaceShopping'),
    path('teamSpaceLodging/scrapList/', teamSpaceLodgingScrapView.as_view(), name='teamLodgingScrapList'),
    path('teamSpaceRecreation/scrapList/', teamSpaceRecreationScrapView.as_view(), name='teamRecreationScrapList'),
]