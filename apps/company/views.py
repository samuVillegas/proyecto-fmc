from django.shortcuts import render, redirect
from apps.company.utilities.choose_type.Group import getQuestions

from .models import Building

# Create your views here
def index(request):
    return render(request,"pages/index.html")

def site_parameterization(request):
    current_question = getQuestions([])
    return render(request,"pages/site_parameterization.html",{'current_question':current_question})

def site_parameterization_from_edit(request, building_id, building_name):
    current_question = getQuestions([])
    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id': building_id, 'building_name': building_name})

def search_building(request):
    buildings_list = Building.objects.all()
    return render(request,"pages/search_building.html", {"buildings_list":buildings_list})

def search_key(request, building_id, building_name):
    current_ids = request.POST.get('current_ids')
    split_current_ids = current_ids.split(',')
    current_question = getQuestions(split_current_ids)
    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id':building_id, 'building_name':building_name})

def site_information(request):
    return render(request,"pages/site_information.html")

def add_building(request):
    site_name = request.POST['site_name']
    address = request.POST['address']
    contact_email = request.POST['contact_email']
    contact_mobile_number = request.POST['contact_mobile_number']

    building = Building.objects.create(
            site_name=site_name,address=address,contact_email=contact_email, contact_mobile_number=contact_mobile_number)

    return redirect('/company/search_building')

def edition_building(request, building_id):
    building = Building.objects.get(code=building_id)
    return render(request, "pages/edit_building.html", {'building':building})

def edit_building(request, building_id):
    site_name = request.POST['site_name']
    address = request.POST['address']
    contact_email = request.POST['contact_email']
    contact_mobile_number = request.POST['contact_mobile_number']

    building = Building.objects.get(code=building_id)
    building.site_name = site_name
    building.address = address
    building.contact_email = contact_email
    building.contact_mobile_number = contact_mobile_number
    building.save()

    return redirect('/company/search_building')

def add_building_type(request):
    site_name = request.POST['site_name']
    address = request.POST['address']
    contact_email = request.POST['contact_email']
    contact_mobile_number = request.POST['contact_mobile_number']

    building = Building.objects.create(
            site_name=site_name,address=address,contact_email=contact_email, contact_mobile_number=contact_mobile_number)
    current_question = getQuestions([])
    return render(request,"pages/site_parameterization.html",{'building_id': building.code, 'building_name': site_name, 'current_question':current_question})

def set_building_type(request, building_id, building_type):
    building = Building.objects.get(code=building_id)
    building.site_type = building_type
    building.save()

    return redirect('/company/search_building')

def delete_building(request, building_id):
    building = Building.objects.get(code=building_id)
    building.delete()

    return redirect('/company/search_building')

def view_building_information(request, building_id):
    building = Building.objects.get(code=building_id)

    return render(request, "pages/view_building_information.html", {'building':building})
