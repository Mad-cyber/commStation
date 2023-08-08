from django.contrib import admin
from django.urls import path, include 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),

    path ('marketplace/', include('marketplace.urls')),

    #cart page
    path('cart/', MarketplaceViews.cart, name='cart'),

    #search path 
    path('search/', MarketplaceViews.search, name='search'),

    #checkout
    path('checkout/', MarketplaceViews.checkout, name= 'checkout' ),

    #ordering
    path('orders/', include('orders.urls')),
         
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
