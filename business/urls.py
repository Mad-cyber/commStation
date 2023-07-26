from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.bussDash, name='business'),
    path('profile/', views.b_profile, name='b_profile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.menuItem_by_category, name='menuItem_by_category'),

    #create cat CRUD
    path('menu_builder/category/add/', views.add_category, name= 'add_category'),
    path('menu_builder/category/edit/<int:pk>', views.edit_category, name= 'edit_category'),
    path('menu_builder/category/edelete/<int:pk>', views.delete_category, name= 'delete_category'),


]