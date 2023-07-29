from django.shortcuts import render, get_object_or_404
from business.models import Business
from menu.models import Category, menuItem
from django.db.models import Prefetch

# Create your views here.
def marketplace(request):
    businesses = Business.objects.filter(is_approved=True, user__is_active=True)
    business_count = businesses.count()

    context = {
        'businesses': businesses,
        'business_count': business_count,
    }

    return render(request, 'marketplace/listings.html', context)

def business_detail(request, bus_slug):
    business = get_object_or_404(Business, bus_slug=bus_slug)

    categories = Category.objects.filter(business=business).prefetch_related(
        Prefetch(
         'menuitems',
         queryset= menuItem.objects.filter(is_available=True)
        )
    )

    context = {
        'business':business,
        'categories': categories,
    }
    return render(request, 'marketplace/business_detail.html', context)



