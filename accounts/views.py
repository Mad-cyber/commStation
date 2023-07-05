from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages

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


    

