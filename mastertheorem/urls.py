# mastertheorem/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.evaluate_view, name='evaluate_master_theorem'),
]