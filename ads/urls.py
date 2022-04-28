from django.urls import path
from .views import analysis_detail

urlpatterns = [
    path('analysis-detail', analysis_detail),
]
