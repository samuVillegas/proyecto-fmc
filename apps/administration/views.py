from django.shortcuts import render
from apps.company.models import Address, Building
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Create your views here.

@login_required
def index(request):
    return render(request,"pages/index_admin.html")

@login_required
def map_building(request):
    address_list = Address.objects.all()
    data = []
    for addr in address_list:
        data.append({"lat":addr.lat,"lng":addr.lng})

    return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")
    
@login_required
def buildings(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        buildings_list = Building.objects.filter(site_name__icontains=searchTerm)
    else:
        buildings_list = Building.objects.all()
    return render(request,"pages/buildings.html",{"buildings_list":buildings_list})

@login_required
def inspectors(request):
    return render(request,"pages/inspectors.html")

@login_required
def regulations(request):
    return render(request,"pages/regulations.html")
