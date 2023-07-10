from django.shortcuts import render , redirect
from django.http import HttpResponse

from business.forms import BussForm
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied

# Create your views here.

#restrict user access to wrong dashbaords
def check_role_buss(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# create user with form from website
def registerUser(request):
    context = {}
    if request.user.is_authenticated:
        messages.warning(request, 'You have already logged into your account')
        return redirect('dashboard')

    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)  # Create a User instance without saving to the database
            # user.set_password(password)
            # user.role = User.CUSTOMER  # Assign the role to the user
            # user.save()  # Save the user to the database

            #create user from create usert method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            #phone_Number = form.cleaned_data['phone_Number']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.role = User.CUSTOMER  # Assign the role to the user
            user.save()
            messages.success(request, 'Your accounts has been registered!')
            return redirect('registerUser')
        else:
            print('invalid entry')
            print(form.errors)
        
    else:
        form = UserForm()

    context['form'] = form
    return render(request, 'accounts/registerUser.html', context)

def registerBusiness(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You have already logged into your account')
        return redirect('dashboard')
    elif request.method =='POST':
        #store data and creare the business
        form = UserForm(request.POST)
        b_form = BussForm(request.POST)
        if form.is_valid() and b_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.role = User.BUSINESS
            user.save()
            business = b_form.save(commit=False)
            business.user = user
            user_profile = userProfile.objects.get(user=user)
            business.user_profile = user_profile 
            business.save()
            messages.success(request, 'Your business has been saved sucesfully and is now under approval')
            return redirect('registerBusiness')
        else: 
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        b_form = BussForm()

    context = {
        'form': form,
        'b_form': b_form,

    }
    return render (request, 'accounts/registerBusiness.html', context)
# manage form details for login, logour and loop incase of error or mistype of passowrd

#manages the pages based on the user roles and permissions for logging in
def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You have already logged into your account')
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)  # Rename the function call to auth_login
            messages.success(request, 'You have successfully logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login details. Please check and try again.')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You have logged out succesfully')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_buss)
def bussDash(request):
    return render(request, 'accounts/bussDash.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDash(request):
    return render(request, 'accounts/custDash.html')










    

