# mastertheorem/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.evaluate_view, name='evaluate_master_theorem'),
    path('api/algorithms/', views.AlgorithmList.as_view(), name="algorithm-list"),
    path('api/evaluate/', views.EvaluateMasterTheoremAPIView.as_view(), name="evaluate-master-theorem-api"),
]