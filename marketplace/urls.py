from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:bus_slug>/', views.business_detail, name='business_detail'),

    #create cart for services
    path('add_to_cart/<int:menu_id>/', views.add_to_cart, name='add_to_cart'),
]
