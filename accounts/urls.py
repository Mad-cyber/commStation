from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerBusiness/', views.registerBusiness, name='registerBusiness'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Updated URL pattern for dashboard
]
