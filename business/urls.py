from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.bussDash, name='business'),
    path('profile/', views.b_profile, name='b_profile'),

]