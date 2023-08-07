from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import userProfile
from business.models import Business, OpenHours
from menu.models import Category, menuItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from datetime import date, datetime
from orders.forms import OrderForm



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

    open_hours = OpenHours.objects.filter(business=business).order_by('day', '-from_hour', '-to_hour')

    today_date = date.today()
    today = today_date.isoweekday()  
    current_opening_hours = OpenHours.objects.filter(business=business, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'business': business,
        'categories': categories,
        'cart_items': cart_items,
        'open_hours': open_hours,
        'current_opening_hours': current_opening_hours,
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
                    return JsonResponse({'status':'Success', 'message': 'Increased the cart quantity!', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, menuitem=menuitem, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'Item added sucessfully to cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                
            except:
                return JsonResponse({'status':'Failed', 'message': 'This item is not in your cart'})

        return JsonResponse({'status':'Failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status':'login_required', 'message': 'Please login to continue'})
    

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
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message': 'This item is not in your cart', 'qty': checkCart.quantity })
                
            except:
                return JsonResponse({'status':'Failed', 'message': 'This item is not in your cart'})

        return JsonResponse({'status':'Success', 'message': 'invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message': 'Please login to continue'})
    
    #return JsonResponse({'status':'Failed', 'message': 'Please loging to continue'})

@login_required(login_url ='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') =='XMLHttpRequest':
          try:
              #check item is active in the cart
              cart_item = Cart.objects.get(user=request.user, id=cart_id)
              if cart_item:
                  cart_item.delete()
                  return JsonResponse({'status':'Success', 'message': 'Cart Item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
          except:
              return JsonResponse({'status':'Failed', 'message': 'This item is not in your cart'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'invalid request'})


def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:

    # print(request.GET)
        address = request.GET['address']
        longitude = request.GET['lng']
        latitude = request.GET['lat']
        radius = request.GET['radius']
        search_word = request.GET['search_word']

        # get the menu items ids for searching
        get_bus_by_service_item = menuItem.objects.filter(menu_title__icontains=search_word, is_available=True).values_list('business',flat=True)
        businesses = Business.objects.filter(Q(id__in=get_bus_by_service_item) | Q(bus_name__icontains=search_word, is_approved=True, user__is_active=True))
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

            
            businesses = Business.objects.filter(Q(id__in=get_bus_by_service_item) | Q(bus_name__icontains=search_word, is_approved=True, user__is_active=True), 
            user_profile__location__distance_lte=(pnt, D(km=radius))
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

            for b in businesses:
                b.kms = round(b.distance.km, 1)
            
        business_count = businesses.count()

        context = {
            'businesses':businesses,
            'business_count':business_count,
            'source_location':address ,
        }

        return render(request, 'marketplace/listings.html', context)
    
@login_required(login_url ='login')
def checkout (request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    user_profile = userProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_Number,
        'email': request.user.email,
        'address': user_profile.address,
        'city': user_profile.city,
        'country':user_profile.country, 
        'post_code':user_profile.post_code,

    }


    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items':cart_items,

    }
    return render(request,'marketplace/checkout.html', context)



