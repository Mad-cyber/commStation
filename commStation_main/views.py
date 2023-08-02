from django.shortcuts import render
from django.http import HttpResponse

from business.models import Business
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def get_or_set_current_location(request):
    if 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat']=lat
        request.session['lng']=lng
        return lng, lat
    else:
         return None

def home(request):
    if get_or_set_current_location(request) is not None:

        pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))

            
        businesses = Business.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1000))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

        for b in businesses:
                b.kms = round(b.distance.km, 1)
    else:
        
        businesses = Business.objects.filter(is_approved=True, user__is_active=True)[:7]
    # print(businesses)
    context = {
        'businesses': businesses,
    }
    return render(request, 'home.html', context)