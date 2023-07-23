from business.models import Business

def get_business(request):
    try:
        business = Business.objects.get(user=request.user)
    except: 
        business = None
    return dict(business=business)