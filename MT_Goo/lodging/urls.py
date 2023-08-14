from django.urls import path
from .views import lodgingMainView, createLodgingView, lodgingDetailView, createReviewView, lodgingScrapView, lodgingReviewListView, myPageLodgingScrapView, editReviewView, mainPageLodgingView

urlpatterns = [
    path('main/', lodgingMainView.as_view(), name='lodgingMain'),
    path('create/', createLodgingView.as_view(), name='createLodging'),
    path('detail/<int:pk>/', lodgingDetailView.as_view(), name='lodgingDetail'),
    path('detail/<int:pk>/review/', lodgingReviewListView.as_view(), name='lodgingReviewListView'),
    path('createReview/', createReviewView.as_view(), name='reviewCreate'),
    path('review/<int:pk>/', editReviewView.as_view(), name='reviewMain'),
    path('scrap/', lodgingScrapView.as_view(), name='createScrap'),
    path('scrapList/', myPageLodgingScrapView.as_view(), name='myPageLodgingScrap'),
    path('mainPage/', mainPageLodgingView.as_view(), name='mainPageLodging'),
]
