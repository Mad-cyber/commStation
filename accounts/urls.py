from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('registerUser/', views.registerUser, name='registerUser'),
]
