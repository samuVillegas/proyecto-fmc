from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Building
from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.data_flow.DataFlow import getQuestions as getQuestionsInsp
from apps.company.utilities.input_request import get_building_information

def index(request):
    return render(request,"pages/index.html")

#def site_parameterization(request):
 #   current_question = getQuestions([])
  #  is_material_list = False

   # return render(request,"pages/site_parameterization.html",{'current_question':current_question, "is_material_list": is_material_list})

def choose_regulation(request, building_name, building_type, building_id):
    building = Building.objects.get(code=building_id)
    building.site_type = building_type
    building.save()

    return render(request, "pages/site_choose_regulation.html",{'building_id': building_id, 'building_name': building_name, 'building_type': building_type})

def site_national_inspection(request, building_name, building_type, building_id):
    #current_question = getQuestionsInsp([], building_type)
    #print(current_question)
    return render(request,"pages/site_inspection.html", {'building_id': building_id, 'building_name': building_name, 'building_type': building_type, "is_national_regulation": True, "current_question":current_question})

def site_parameterization_from_edit(request, building_id, building_name, building_regulation):
    current_question = getQuestions([], building_regulation)
    is_material_list = False
    return render(request,"pages/site_parameterization.html", {'current_question':current_question , 'building_id':building_id,
                    'building_name': building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

def search_building(request):
    searchTerm = request.GET.get('searchTerm')

    if searchTerm:
        buildings_list = Building.objects.filter(site_name__icontains=searchTerm)
    else:
        buildings_list = Building.objects.all()

    return render(request,"pages/search_building.html", {"buildings_list":buildings_list, "searchTerm":searchTerm   })

def search_key(request, building_id, building_name, building_regulation):
    current_ids = request.POST.get('current_ids')
    split_current_ids = current_ids.split(',')
    current_question = getQuestions(split_current_ids, building_regulation)
    #is_material_list = False
    try:
        if 'img' not in current_question['image']:
            is_material_list = True
            current_question['image'] = current_question['image'].split(';')
    except:
        is_material_list = False
    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id':building_id, 'building_name':building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

def search_flow(request, building_id, building_name, building_type):
    current_ids = request.POST.get('current_ids_flow')
    split_current_ids = current_ids.split(',')
    current_question = getQuestionsInsp(split_current_ids, building_type)
    return render(request,"pages/site_inspection.html",{'current_question':current_question, 'building_id':building_id, 'building_name':building_name, "building_type": building_type})

def site_information(request):
    return render(request,"pages/site_information.html")

def add_building(request):
    building_information_list = get_building_information(request)
    
    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != '' and request.POST['address'] != '' and request.POST['contact_email'] != '':
        building = Building.objects.filter(site_name__iexact=building_information_list[0])
        if building:
            messages.error(request, 'Edificio ya existe')
        else:
            regulation_re = request.POST['sel_regulation']
            Building.objects.create(site_name=building_information_list[0],address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3], regulation=regulation_re)
            messages.success(request, 'Edificio creado con exito')
    else:
        messages.error(request, 'Por favor llenar todos los campos')
        return render(request, 'pages/site_information.html', 
                      {'building_name': building_information_list[0], 'building_address': building_information_list[1], 
                      'building_email': building_information_list[2],'building_number': building_information_list[3]})
    return render (request, 'pages/site_information.html')

def edition_building(request, building_id):
    building = Building.objects.get(code=building_id)
    return render(request, "pages/edit_building.html", {'building':building})

def edit_building(request, building_id):
    building_information_list = get_building_information(request)

    regulation_req = request.POST['sel_regulation']
    building = Building.objects.get(code=building_id)

    if regulation_req != building.regulation:
        building.site_type = None
        messages.error(request, 'Se cambio la normativa: Debe categorizar de nuevo el edificio')

    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != '' and request.POST['address'] != '' and request.POST['contact_email'] != '':
        building.site_name = building_information_list[0]
        building.address = building_information_list[1]
        building.contact_email = building_information_list[2]
        building.contact_mobile_number = building_information_list[3]
        building.regulation = regulation_req
        building.save()
        messages.success(request, 'Edificio editado con exito')
    else: 
        messages.error(request, 'Por favor llenar todos los campos')
    
    return redirect('/company/search_building')
    
def add_building_type(request):
    building_information_list = get_building_information(request)
    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != ' ' and request.POST['address'] != '' and request.POST['contact_email'] != '':
        building = Building.objects.filter(site_name__iexact=building_information_list[0])
        if building:
            messages.error(request, 'Edificio ya existe')
        else:
            regulation_re = request.POST['sel_regulation']
            b = Building.objects.create(site_name=building_information_list[0],address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3],regulation=regulation_re)
            current_question = getQuestions([], b.regulation)
            return render(request,"pages/site_parameterization.html",{'building_id': b.code, 'building_name': b.site_name, 'building_regulation': b.regulation, 'current_question':current_question})
    else:
        messages.error(request, 'Por favor llenar todos los campos')
        return render(request, 'pages/site_information.html', 
                      {'building_name': building_information_list[0], 'building_address': building_information_list[1], 
                      'building_email': building_information_list[2],'building_number': building_information_list[3]})
    return render (request, 'pages/site_information.html')

def set_building_type(request, building_id, building_type):
    building = Building.objects.get(code=building_id)
    building.site_type = building_type
    building.save()

    messages.success(request, 'Edificio creado con caracterizacion')
    return redirect('/company/search_building')

def delete_building(request):
    code_building = request.POST.get('delete_id_item')
    building = Building.objects.get(code=code_building)
    building.delete()

    messages.success(request, 'Edificio eliminado con exito')
    return redirect('/company/search_building')

def view_building_information(request, building_id):
    building = Building.objects.get(code=building_id)

    return render(request, "pages/view_building_information.html", {'building':building})