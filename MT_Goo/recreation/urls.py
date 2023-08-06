from django.urls import path
from .views import createRecreationView, recreationMainView

urlpatterns = [
    path('create/', createRecreationView.as_view(), name='createRecreation'),
    path('main/', recreationMainView.as_view(), name='recreationMain'),
]
