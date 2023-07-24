from business.models import Business
from django.conf import settings

def get_business(request):
    try:
        business = Business.objects.get(user=request.user)
    except: 
        business = None
    return dict(business=business)

def get_google_api(request):
    return{'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}