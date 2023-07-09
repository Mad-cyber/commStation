from django.shortcuts import render , redirect
from django.http import HttpResponse

from business.forms import BussForm
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages, auth

# Create your views here.
# create user with form from website
def registerUser(request):
    context = {}

    if request.method == 'POST':
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
    if request.method =='POST':
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

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login details. Please check your details and try again')
            return redirect('login')

    return redirect('login')  # Redirect to the login page if the request method is not POST

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out.')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')



    

