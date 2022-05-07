from django.shortcuts import render
from apps.company.models import Building
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request,"pages/index_admin.html")

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
