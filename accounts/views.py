from django.shortcuts import render , redirect
from django.http import HttpResponse

from business.forms import BussForm
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login
from .utils import detectUser, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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

            #send email verifcation
            send_verification_email(request, user)

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

            #send verifcation email business 
            send_verification_email(request,user)

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

def activate(request, uidb64, token ):
    #activate user email from token vertifcation(setting =True)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been sucessfully verifed and is now active! Thank you for your interest')
        return redirect ('myAccount')
    else:
        messages .error(request, 'invalid link, please try again')
        return redirect ('myAccount')
    


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
# manage user accounts, reset password, login and register
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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)    

            #send reset password email
            send_password_reset_email(request, user)

            messages.success(request, 'You password reset link has been sent to the added email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist. Please recheck your email address')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    #validate user by decoding the token and primary key
    return

def reset_password(request):
    return render(request, 'accounts/reset_password.html')










    

