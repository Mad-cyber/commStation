from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    
    path('<slug:bus_slug>/', views.business_detail, name='business_detail'),
    

    #create cart for services
    #increase cart
    path('add_to_cart/<int:menu_id>/', views.add_to_cart, name='add_to_cart'),
    #decrease cart
    path('remove_cart_item/<int:menu_id>/', views.remove_cart_item, name='remove_cart_item'),
    #delete the cart items from the cart page
    path ('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

    
]
