from django.urls import path
from .views import lodgingMainView, CreateLodgingView, lodgingDetailView, CreateReviewView

urlpatterns = [
    path('main/', lodgingMainView.as_view(), name='lodgingMain'),
    path('create/', CreateLodgingView.as_view(), name='create-lodging'),
    path('detail/<int:pk>/', lodgingDetailView.as_view(), name='lodgingDetail'),
<<<<<<< Updated upstream
    path('create_review/', CreateReviewView.as_view(), name='createReview'),
=======
    path('createReview/', createReviewView.as_view(), name='createReview'),
    path('scrap/', lodgingScrapView.as_view(), name='createScrap'),
>>>>>>> Stashed changes
]
