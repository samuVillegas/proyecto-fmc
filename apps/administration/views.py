from django.shortcuts import render
from apps.company.models import Building
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import json
# Create your views here.

@login_required
def index(request):
    return render(request,"pages/index_admin.html")

@login_required
def dashboard_char_regulation(request):
    nationalBuildings = Building.objects.filter(regulation='NSR10')
    internationalBuildings = Building.objects.filter(regulation='NFPA101')
    data = [len(nationalBuildings),len(internationalBuildings)]
    return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")

@login_required
def dashboard_buildings_by_type(request):
    buildings = Building.objects.raw('SELECT count(site_type)  AS cantidad, site_type, code FROM company_building GROUP BY site_type;')
    data = []
    for p in buildings:
        data.append({"site_type":p.site_type,"cantidad":p.cantidad})
    return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")

@login_required
def dashboard_building_inspection_state(request):
    buildings = Building.objects.raw('''
    SELECT ci.code, count(is_inspection_successful) cantidad, is_inspection_successful valor FROM company_building cb
    LEFT JOIN company_inspection ci ON ci.building_id = cb.code
    GROUP BY is_inspection_successful;
    '''); 

    data = [0,0,0];
    for p in buildings:
        if p.valor == 1:
            data[0] = p.cantidad
        elif p.valor == 0:
            data[1] = p.cantidad
        else:
            data[2] = p.cantidad
    return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")

@login_required
def buildings(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        buildings_list = Building.objects.filter(site_name__icontains=searchTerm)
    else:
        buildings_list = Building.objects.all()
    return render(request,"pages/buildings.html",{"buildings_list":buildings_list,'searchTerm':searchTerm})

@login_required
def inspectors(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        inspectors = User.objects.filter(Q(first_name__contains=searchTerm) | Q(last_name__contains=searchTerm) | Q(email__contains=searchTerm))
    else:
        inspectors = User.objects.filter(is_superuser=0)
    return render(request,"pages/inspectors.html",{'inspectors':inspectors,'searchTerm':searchTerm})

@login_required
def regulations(request):
    return render(request,"pages/regulations.html")
