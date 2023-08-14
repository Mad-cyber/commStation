from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order, OrderedItem
from .forms import BussForm, OpenHoursForm
from accounts.forms import UserProfileForm
from django.db import IntegrityError

from accounts.models import userProfile
from .models import Business, OpenHours
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_buss

from menu.models import Category, menuItem
from menu.forms import CategoryForm, menuItemForm
from django.template.defaultfilters import slugify

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
    categories = Category.objects.filter(business=business).order_by('created_at')
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

from django.db import IntegrityError

@login_required(login_url='login')
@user_passes_test(check_role_buss)
def add_category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.business = get_business(request)
            
            try:
                category.save()
                category.slug = slugify(category_name)+'-'+str(category.id)#pizaa-10
                category.save()
                messages.success(request, 'New Category has been created sucessfully!')
                return redirect('menu_builder')
            except IntegrityError:
                form.add_error(None, "A category with this slug already exists.")
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'business/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_buss)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method =='POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.business = get_business(request)
            category.slug = slugify(category_name)
            try:
                form.save()
                messages.success(request, 'Category has been updated sucessfully!')
                return redirect('menu_builder')
            except IntegrityError:
                form.add_error(None, "A category with this slug already exists.")
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }

    return render(request, 'business/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_buss)
def delete_category(request,pk=None):
    category =get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted!')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_buss)
def add_menu(request):
    if request.method =='POST':
        form = menuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_title = form.cleaned_data['menu_title']
            menu = form.save(commit=False)
            menu.business = get_business(request)
            menu.slug = slugify(menu_title)
            try:
                form.save()
                messages.success(request, 'New Service Item has been created sucessfully!')
                return redirect('menuItem_by_category', menu.category.id)
            except IntegrityError:
                form.add_error(None, "A service with this slug already exists.")
    else:
        form = menuItemForm()
    context = {
        'form': form,
    }
    form = menuItemForm()
    #modify category form so it shows for the business only
    form.fields['category'].queryset = Category.objects.filter(business=get_business(request))
    context = {
        'form': form,
    }
    return render(request, 'business/add_menu.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_buss)
def edit_menu(request, pk=None):
    menu_item = get_object_or_404(menuItem, pk=pk)
    if request.method == 'POST':
        form = menuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            menu_title = form.cleaned_data['menu_title']
            menu_item = form.save(commit=False)
            menu_item.business = get_business(request)
            menu_item.slug = slugify(menu_title)
            try:
                form.save()
                messages.success(request, 'Service has been updated successfully!')
                return redirect('menuItem_by_category', menu_item.category.id) 
            except IntegrityError:
                form.add_error(None, "A service with this slug already exists.")
    else:
        form = menuItemForm(instance=menu_item)
        #modify category form so it shows for the business only
    form.fields['category'].queryset = Category.objects.filter(business=get_business(request))
    context = {
        'form': form,
        'menu_item': menu_item,  
    }

    return render(request, 'business/edit_menu.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_buss)
def delete_menu(request,pk=None):
    menu_item =get_object_or_404(menuItem, pk=pk)
    category_id = menu_item.category.id
    menu_item.delete()
    messages.success(request, 'This menu item has been deleted sucessfully!')
    return redirect('menuItem_by_category', category_id)


def open_hours(request):
    open_hours = OpenHours.objects.filter(business=get_business(request))
    form = OpenHoursForm()
    context = {
        'form': form,
        'open_hours': open_hours,
    }

    return render (request, 'business/open_hours.html', context)

def add_open_hours(request):
    #handle the request for the open hours function in custom.js and save in db
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            # print(day, from_hour, to_hour, is_closed)

            try:
                hour = OpenHours.objects.create(business=get_business(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpenHours.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id':hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'}
                    else:
                        response = {'status': 'success', 'id':hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                
                return JsonResponse(response) 
            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' is active for this day. Please add a different day for your schedule.', 'error': str(e)}
                return JsonResponse(response)                                  
            
        else:
            HTTPResponse('invalid request')

def remove_open_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpenHours, pk=pk,)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})
        

def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        #print(order)
        ordered_item = OrderedItem.objects.filter(order=order, menuitem__business=get_business(request))
        # print(ordered_item)
        context = {
            'order': order,
            'ordered_item': ordered_item,
             
        }
    except:
        return redirect('business')

    return render(request, 'business/order_detail.html', context)



 







