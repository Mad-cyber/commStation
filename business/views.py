from django.shortcuts import render, get_object_or_404, redirect
from .forms import BussForm
from accounts.forms import UserProfileForm

from accounts.models import userProfile
from .models import Business
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_buss

from menu.models import Category, menuItem

def get_business(request):
    business = Business.objects.get(user=request.user)
    return business

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_buss)
def b_profile(request):
    profile = get_object_or_404(userProfile, user=request.user)
    business = get_object_or_404(Business, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        bus_form = BussForm(request.POST, request.FILES, instance=business)
        if profile_form.is_valid() and bus_form.is_valid():
            profile_form.save()
            bus_form.save()
            messages.success(request, 'Your information has been updated and saved to your Business Account')
            return redirect('b_profile')
        else:
            print(profile_form.errors)
            print(bus_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        bus_form = BussForm(instance=business)


    context = {
        'profile_form':profile_form,
        'bus_form': bus_form,
        'profile': profile,
        'business': business,


    }
    return render(request, 'business/b_profile.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_buss)
def menu_builder(request):
    business = get_business(request)
    categories = Category.objects.filter(business=business)
    context = {
        'categories':categories,

    }
    return render(request, 'business/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_buss)
def menuItem_by_category(request, pk=None):
    business = get_business(request)
    category = get_object_or_404(Category, pk=pk)
    menuitems = menuItem.objects.filter(business=business, category=category)
    context = {
        'menuitems': menuitems,
        'category': category,

    }
    return render (request, 'business/menuItem_by_category.html', context)

def add_category(request):
    return render(request, 'business/add_category.html')
