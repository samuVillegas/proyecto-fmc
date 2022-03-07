from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Building
from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.input_request import get_building_information

def index(request):
    return render(request,"pages/index.html")

def site_parameterization(request):
    current_question = getQuestions([])
    return render(request,"pages/site_parameterization.html",{'current_question':current_question})

def site_parameterization_from_edit(request, building_id, building_name):
    current_question = getQuestions([])
    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id': building_id, 'building_name': building_name})

def search_building(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        buildings_list = Building.objects.filter(site_name__icontains=searchTerm)
    else:
        buildings_list = Building.objects.all()

    return render(request,"pages/search_building.html", {"buildings_list":buildings_list, "searchTerm":searchTerm   })

def search_key(request, building_id, building_name):
    current_ids = request.POST.get('current_ids')
    split_current_ids = current_ids.split(',')
    current_question = getQuestions(split_current_ids)
    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id':building_id, 'building_name':building_name})

def site_information(request):
    return render(request,"pages/site_information.html")

def add_building(request):
    building_information_list = get_building_information(request)
    try:
        Building.objects.filter(site_name__iexact=building_information_list[0]).get()
        messages.error(request, 'Edificio ya existe')
    except:
        try:
            Building.objects.create(site_name=building_information_list[0],address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3])
            messages.success(request, 'Edificio creado con exito')
        except:
            messages.error(request, 'No es posible crear edificio')

    return render(request, 'pages/site_information.html')

def edition_building(request, building_id):
    building = Building.objects.get(code=building_id)
    return render(request, "pages/edit_building.html", {'building':building})

def edit_building(request, building_id):
    building_information_list = get_building_information(request)

    try:
        Building.objects.filter(site_name__iexact=building_information_list[0]).get()
        messages.error(request, 'Existe un edificio con el mismo nombre')
    except:
        building = Building.objects.get(code=building_id)
        building.site_name = building_information_list[0]
        building.address = building_information_list[1]
        building.contact_email = building_information_list[2]
        building.contact_mobile_number = building_information_list[3]
        building.save()
        messages.success(request, 'Edificio editado con exito')

    return redirect('/company/search_building')

def add_building_type(request):
    building_information_list = get_building_information(request)
    building = None

    try:
        Building.objects.filter(site_name__iexact=building_information_list[0]).get()
        messages.error(request, 'Edificio ya existe')
        return render(request, 'pages/site_information.html')
    except:
        try:
            building = Building.objects.create(site_name=building_information_list[0],address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3])
            current_question = getQuestions([])
            return render(request,"pages/site_parameterization.html",{'building_id': building.code, 'building_name': building.site_name, 'current_question':current_question})
        except:
            messages.error(request, 'No es posible crear edificio')
            return render(request, 'pages/site_information.html')

def set_building_type(request, building_id, building_type):
    building = Building.objects.get(code=building_id)
    building.site_type = building_type
    building.save()

    messages.success(request, 'Edificio creado con caracterizacion')
    return redirect('/company/search_building')

def delete_building(request, building_id):
    building = Building.objects.get(code=building_id)
    building.delete()

    messages.success(request, 'Edificio eliminado con exito')
    return redirect('/company/search_building')

def view_building_information(request, building_id):
    building = Building.objects.get(code=building_id)

    return render(request, "pages/view_building_information.html", {'building':building})
