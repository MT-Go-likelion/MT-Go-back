from django.urls import path
from .views import createRecreationView, recreationMainView, recreationScrapView, recreationDetailView, myPageRecreationScrapView, mainPageRecreationView

urlpatterns = [
    path('create/', createRecreationView.as_view(), name='createRecreation'),
    path('main/', recreationMainView.as_view(), name='recreationMain'),
    path('detail/<int:pk>/', recreationDetailView.as_view(),
         name='recreationDetail'),
    path('scrap/', recreationScrapView.as_view(), name='createScrap'),
    path('scrapList/', myPageRecreationScrapView.as_view(), name='scrapList'),
    path('mainPage/', mainPageRecreationView.as_view(), name='mainPageRecreation'),
]
