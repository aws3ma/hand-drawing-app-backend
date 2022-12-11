from .views import ImageView
# from .views import ProductPredictionView
from django.urls import path

urlpatterns = [
    path('',ImageView.as_view(),name='images'),
] 
