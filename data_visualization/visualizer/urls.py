# data_visualization/visualizer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualization, name='visualization'),
]
