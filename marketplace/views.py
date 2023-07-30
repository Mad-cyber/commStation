from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from business.models import Business
from menu.models import Category, menuItem
from django.db.models import Prefetch
from .models import Cart

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

def add_to_cart(request, menu_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') =='XMLHttpRequest':
            #check if item exists before adding to cart
            try:
                menuitem = menuItem.objects.get(id=menu_id)
                #check if user added item to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, menuitem=menuitem)
                    #increase the quanity 
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success', 'message': 'Increased the cart quantity! '})
                except:
                    checkCart = Cart.objects.create(user=request.user, menuitem=menuitem, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'Item added sucessfully to cart'})
                
            except:
                return JsonResponse({'status':'Failed', 'message': 'this menu item does not exist'})

        return JsonResponse({'status':'Success', 'message': 'invalid request'})
    else:
        return JsonResponse({'status':'Failed', 'message': 'Please loging to continue'})



