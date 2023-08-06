from django.urls import path
from .views import createRecreationView, recreationMainView, recreationScrapView, recreationDetailView

urlpatterns = [
    path('create/', createRecreationView.as_view(), name='createRecreation'),
    path('main/', recreationMainView.as_view(), name='recreationMain'),
    path('detail/<int:pk>/', recreationDetailView.as_view(), name='recreationDetail'),
    path('scrap/', recreationScrapView.as_view(), name='createScrap'),
]
