from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('analyze/', views.analyze, name='analyze'),
    path('simulate/', views.simulate_wearable, name='simulate'),
    path('result/', views.result, name='result'),
]
