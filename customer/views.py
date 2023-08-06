from django.shortcuts import render


def cprofile(request):
    return render(request, 'customer/cprofile.html')
