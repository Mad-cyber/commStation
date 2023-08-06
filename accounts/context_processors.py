from business.models import Business
from accounts.models import userProfile
from django.conf import settings

def get_business(request):
    try:
        business = Business.objects.get(user=request.user)
    except: 
        business = None
    return dict(business=business)

def get_user_profile(request):
    try:
        user_profile = userProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_google_api(request):
    return{'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}