from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerBusiness/', views.registerBusiness, name='registerBusiness'),
    # Update the URL pattern to use the login view

    #path('accounts/login/', views.login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDash/', views.custDash, name='custDash'),  # Updated URL pattern for dashboard
    path('bussDash/', views.bussDash, name='bussDash'),  # Updated URL pattern for dashboard
]
