from django.urls import path
from .views import lodgingMainView, createLodgingView, lodgingDetailView, createReviewView

urlpatterns = [
    path('main/', lodgingMainView.as_view(), name='lodgingMain'),
    path('create/', createLodgingView.as_view(), name='createLodging'),
    path('detail/<int:pk>/', lodgingDetailView.as_view(), name='lodgingDetail'),
    path('create_review/', createReviewView.as_view(), name='createReview'),
]
