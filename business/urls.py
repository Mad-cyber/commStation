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
    path('menu_builder/category/delete/<int:pk>', views.delete_category, name= 'delete_category'),

    #create menu item CRUD
    path('menu_builder/menu/add/', views.add_menu, name= 'add_menu'),
    path('menu_builder/menu/edit/<int:pk>', views.edit_menu, name= 'edit_menu'),
    path('menu_builder/menu/delete/<int:pk>', views.delete_menu, name= 'delete_menu'),

    #path for the opening hours page
    path('openhours/', views.open_hours, name= 'open_hours'),
    path('openhours/add/', views.add_open_hours, name ='add_open_hours'),


]