# mastertheorem/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.frontend, name="frontend"),
    path('api/algorithms/', views.AlgorithmList.as_view(), name="algorithm-list"),
    path('api/evaluate/', views.EvaluateMasterTheoremAPIView.as_view(), name="evaluate-master-theorem-api"),
]