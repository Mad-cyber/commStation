from django.shortcuts import render

# Create your views here.
def b_profile(request):
    return render(request, 'business/b_profile.html')
