from django.urls import path
from .views import lodgingMainView, createLodgingView, lodgingDetailView, createReviewView, lodgingScrapView, lodgingReviewView

urlpatterns = [
    path('main/', lodgingMainView.as_view(), name='lodgingMain'),
    path('create/', createLodgingView.as_view(), name='createLodging'),
    path('detail/<int:pk>/', lodgingDetailView.as_view(), name='lodgingDetail'),
    path('detail/<int:pk>/review/', lodgingReviewView.as_view(), name='lodgingReviewView'),
    path('createReview/', createReviewView.as_view(), name='createReview'),
    path('scrap/', lodgingScrapView.as_view(), name='createScrap'),
]
