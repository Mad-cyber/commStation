from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import userProfile
from django.contrib import messages
from orders.models import Order, OrderedItem
import simplejson as json


@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(userProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user) 
        if profile_form.is_valid and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,

    }
    return render(request, 'customer/cprofile.html', context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'customer/my_orders.html', context)

def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_item = OrderedItem.objects.filter(order=order)
        subtotal = 0

        for item in ordered_item:
            subtotal+= (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)

        #print(ordered_item)
        context= {
            'order':order,
            'ordered_item': ordered_item,
            'subtotal':subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'customer/order_detail.html', context)
    except:
        return redirect('customer')
    
