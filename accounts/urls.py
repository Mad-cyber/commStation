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
    path('custDash/', views.custDash, name='custDash'), 
    path('bussDash/', views.bussDash, name='bussDash'),  

    path ('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_validate/<str:uidb64>/<str:token>/', views.reset_password_validate, name='reset_password_validate'),

]
