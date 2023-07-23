from django.shortcuts import render, get_object_or_404, redirect
from .forms import BussForm
from accounts.forms import UserProfileForm

from accounts.models import userProfile
from .models import Business
from django.contrib import messages

# Create your views here.
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
