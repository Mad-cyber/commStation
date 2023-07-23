from django.shortcuts import render, get_object_or_404
from .forms import BussForm
from accounts.forms import UserProfileForm

from accounts.models import userProfile
from .models import Business

# Create your views here.
def b_profile(request):
    profile = get_object_or_404(userProfile, user=request.user)
    business = get_object_or_404(Business, user=request.user)

    profile_form = UserProfileForm(instance = profile)
    bus_form = BussForm(instance=business)

    context = {
        'profile_form':profile_form,
        'bus_form': bus_form,
        'profile': profile,
        'business': business,


    }
    return render(request, 'business/b_profile.html', context)
