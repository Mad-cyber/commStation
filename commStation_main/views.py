from django.shortcuts import render
from django.http import HttpResponse

from business.models import Business

def home(request):
    businesses = Business.objects.filter(is_approved=True, user__is_active=True)[:7]
    # print(businesses)
    context = {
        'businesses': businesses,
    }
    return render(request, 'home.html', context)