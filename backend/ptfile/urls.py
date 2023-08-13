from django.urls import path
from .views import label_image

urlpatterns = [
    path('label/', label_image, name='label'),
]
