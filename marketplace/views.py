from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from business.models import Business
from menu.models import Category, menuItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter

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

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'business':business,
        'categories': categories,
        'cart_items':cart_items,
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
                    return JsonResponse({'status':'Success', 'message': 'Increased the cart quantity!', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})
                except:
                    checkCart = Cart.objects.create(user=request.user, menuitem=menuitem, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'Item added sucessfully to cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity })
                
            except:
                return JsonResponse({'status':'Failed', 'message': 'this menu item does not exist'})

        return JsonResponse({'status':'Success', 'message': 'invalid request'})
    else:
        return JsonResponse({'status':'Failed', 'message': 'Please loging to continue'})
    

def remove_cart_item(request, menu_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') =='XMLHttpRequest':
            #check if item exists before adding to cart
            try:
                menuitem = menuItem.objects.get(id=menu_id)
                #check if user added item to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, menuitem=menuitem)
                    if checkCart.quantity >1:
                        #decrease the cart the quanity 
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})
                except:
                    return JsonResponse({'status':'Failed', 'message': 'This item is not in your cart', 'qty': checkCart.quantity })
                
            except:
                return JsonResponse({'status':'Failure', 'message': 'this menu item does not exist'})

        return JsonResponse({'status':'Success', 'message': 'invalid request'})
    else:
        return JsonResponse({'status':'Failure', 'message': 'Please loging to continue'})
    
    #return JsonResponse({'status':'Failed', 'message': 'Please loging to continue'})



