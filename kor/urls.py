from django.urls import path
from .views import FlagDetectionView

urlpatterns = [
    path('detect/', FlagDetectionView.as_view(), name='flag_detection'),
]