from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:bus_slug>/', views.business_detail, name='business_detail'),
]