from django.shortcuts import render
from apps.company.models import Building
# Create your views here.
def index(request):
    return render(request,"pages/index_admin.html")

def buildings(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        buildings_list = Building.objects.filter(site_name__icontains=searchTerm)
    else:
        buildings_list = Building.objects.all()
    return render(request,"pages/buildings.html",{"buildings_list":buildings_list})

def inspectors(request):
    return render(request,"pages/inspectors.html")

def regulations(request):
    return render(request,"pages/regulations.html")
