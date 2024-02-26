# mastertheorem/urls.py

from django.urls import path
from . import views
from .views import AlgorithmList

urlpatterns = [
    path('', views.evaluate_view, name='evaluate_master_theorem'),
    path('api/algorithms/', AlgorithmList.as_view(), name="algorithm-list")
]