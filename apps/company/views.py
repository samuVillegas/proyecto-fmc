from cgi import print_directory
from contextlib import nullcontext
from typing import final
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings 
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import re
import os
import json 

from matplotlib.style import context
from geopy.geocoders import Nominatim
import geocoder
import folium

from matplotlib import image
from numpy import append

from .models import Building, Inspection, Address
from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.data_flow.DataFlow import getQuestions as getQuestionsInsp
from apps.company.utilities.input_request import get_building_information
from apps.company.utilities.choose_type.Group import readFile as readFileType
from apps.company.utilities.data_flow.DataFlow import readFile as readFileIns
from apps.company.utilities.data_flow.Question import Question
from apps.company.utilities.forms import ContactForm
from apps.company.utilities.data_flow.DataFlow import getQuestionsFlow, writeFileFlow
from apps.company.utilities.choose_type.Group import getQuestionsGroup, writeFileGroup

@login_required
def index(request):
    #print(request.user.get_full_name())
    return render(request,"pages/index.html")

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")
    
#def site_parameterization(request):
 #   current_question = getQuestions([])
  #  is_material_list = False

   # return render(request,"pages/site_parameterization.html",{'current_question':current_question, "is_material_list": is_material_list})

#def choose_regulation(request, building_name, building_type, building_id):
 #   building = Building.objects.get(code=building_id)
  #  building.site_type = building_type
   # building.save()

    #return render(request, "pages/site_choose_regulation.html",{'building_id': building_id, 'building_name': building_name, 'building_type': building_type})

#def site_national_inspection(request, building_name, building_type, building_id):
    #current_question = getQuestionsInsp([], building_type)
    #print(current_question)
 #   return render(request,"pages/site_inspection.html", {'building_id': building_id, 'building_name': building_name, 'building_type': building_type, "is_national_regulation": True, "current_question":current_question})

@login_required
def site_inspection(request, building_name, building_type, building_regulation):
    building = Building.objects.get(site_name=building_name)
    building.site_type = building_type
    building.save()
    is_material_list = None
    current_question =  getQuestionsInsp([], building_regulation, building_type)
    try:
        if 'img' not in current_question['image']:
            is_material_list = True
            current_question['image'] = current_question['image'].split(';')
    except:
        try:
            if current_question['image'] != '[]':
                is_material_list = False
        except:
            is_material_list = None
    #print(current_question)
    return render(request, "pages/site_inspection.html", {'current_question':current_question, 'building_name': building_name, 'building_type': building_type, 'building_regulation': building_regulation, 'is_material_list':is_material_list})

@login_required
def site_parameterization_from_edit(request,building_name, building_regulation):
    current_question = getQuestions([], building_regulation)
    is_material_list = False
    return render(request,"pages/site_parameterization.html", {'current_question':current_question,
                    'building_name': building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

@login_required
def search_building(request):
    searchTerm = request.GET.get('searchTerm')
    inspections_list = []
    list = []

    if searchTerm:
        try:
            buildings = Building.objects.get(site_name__icontains=searchTerm)
            inspections = Building.objects.get(site_name=buildings.site_name).inspection_set.all()
            if(len(inspections) > 0):
                inspection = inspections[len(inspections) - 1]
                list.append([buildings,inspection])
            else:
                list.append([buildings,''])
        except:
            list = []
    else:
        buildings_list = Building.objects.all()
        inspections_list = Inspection.objects.all()

        for b in buildings_list:
            inspections = Building.objects.get(site_name=b.site_name).inspection_set.all()
            if(len(inspections) > 0):
                inspection = inspections[len(inspections) - 1]
                list.append([b,inspection])
            else:
                list.append([b,''])

    return render(request,"pages/search_building.html", {"inspections_list":inspections_list, "list": list, "searchTerm":searchTerm})

@login_required
def search_key(request, building_name, building_regulation):
    current_ids = request.POST.get('current_ids')

    split_current_ids = current_ids.split(',')

    current_question = None
    is_material_list = None
    #print(len(split_current_ids))
    #print(split_current_ids)
    if split_current_ids != ['']:
        current_question = getQuestions(split_current_ids, building_regulation)
        #is_material_list = False
        try:
            if 'img' not in current_question['image']:
                is_material_list = True
                current_question['image'] = current_question['image'].split(';')
        except:
            is_material_list = False
    else:
        current_question = getQuestions([], building_regulation)

    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_name':building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

@login_required
def search_flow(request, building_name, building_type, building_regulation):
    current_ids = request.POST.get('current_ids_flow')
    split_current_ids = current_ids.split(',')
    #print(split_current_ids)
    is_material_list = False

    if split_current_ids != ['']:
        current_question = getQuestionsInsp(split_current_ids, building_regulation, building_type)
        try:
            if 'img' not in current_question['image']:
                is_material_list = True
                current_question['image'] = current_question['image'].split(';')
        except:
            try:
                if current_question['image'] != '[]':
                    is_material_list = False
            except:
                is_material_list = None
    else:
        current_question = getQuestionsInsp([], building_regulation, building_type)

    #print(is_material_list)
    #print(type(current_question['image']))
    return render(request,"pages/site_inspection.html",{'current_question':current_question, 'building_regulation': building_regulation, 'building_name':building_name, "building_type": building_type, 'is_material_list': is_material_list})

@login_required
def check_inspection(request, building_name):
    current_final_ids = request.POST.get('ids_final_flow')
    final_flow = request.POST.get('final_flow')

    if current_final_ids != None:
        current_final_ids = current_final_ids.split(',')

    if final_flow != None:
        final_flow = re.sub("\[|\]","",final_flow)
        final_flow = final_flow.split("', ")

        for ite, d in enumerate(final_flow):
            final_flow[ite] = re.sub("\'","",d)
    #print(current_final_ids)

    is_inspection_succesfull = False
    #print(final_flow)
    #print(current_final_ids)
    if(current_final_ids != ['']) or (final_flow == None):
        if final_flow == None:
            is_inspection_succesfull = True
        elif len(current_final_ids) == len(final_flow):
            is_inspection_succesfull = True

    #print(is_inspection_succesfull)
    #print(len(current_final_ids))
    
    if current_final_ids != None and current_final_ids != ['']:
        for id in current_final_ids:
            if int(id) - 1 < len(current_final_ids):
                final_flow[int(id) - 1] = ''

    #print(final_flow)
    if final_flow != None:
        for ite,ef in enumerate(final_flow):
            if ef == '':
                final_flow.pop(ite)

    #print(final_flow)

    #print(final_flow)
    username = request.user.get_full_name()
    b = Building.objects.filter(site_name__iexact=building_name).get()
    b.modificated_by = username
    b.save()
    Inspection.objects.create(description=final_flow, is_inspection_successful=is_inspection_succesfull, building=b, inspected_by=username, site_type=b.site_type)
    return redirect('/company/search_building')

@login_required
def site_information(request):
    '''location = geocoder.osm('Calle 78B 69-240 0500 Medellín Antioquia Colombia')
    print(location)'''
    '''Nomi_locator = Nominatim(user_agent="My App")

    address= "Calle 78 B NO. 69 - 240 Medellín, Colombia"

    #get the location detail 
    location = Nomi_locator.geocode(address)

    print("You find for the location:", location)'''
    
    '''map = folium.Map(location=[6.2402, -75.5767], zoom_start=13)
    #popup1 = folium.LatLngPopup()

    #map.add_child(popup1)
    #print("Latitude of Popup: ", popup1) 
    
    #map = folium.Map(location=[19, -12], zoom_start=2)
    #folium.Marker([], tooltip='Ver', popup="Carrera 49, Cl. 7 Sur #50, Medellín, Antioquia").add_to(map)
    map = map._repr_html_()'''
    return render(request,"pages/site_information.html")

'''@login_required
def search_in_map(request):
    site_name = request.POST['site_name']
    address = request.POST['address']
    contact_email = request.POST['contact_email']
    contact_mobile_number = request.POST['contact_mobile_number']
    
    map = folium.Map(location=[6.2402, -75.5767], zoom_start=10)
    popup1 = folium.LatLngPopup()
    print(popup1)
    location = geocoder.osm(address)
    if location != None:
        lat = location.lat
        lng = location.lng
        folium.Marker([lat, lng], tooltip='ver', popup=address).add_to(map)

    map = map._repr_html_()

    context = {
        'map': map,
        'building_name': site_name,
        'building_address':address,
        'building_email': contact_email,
        'building_number': contact_mobile_number,
    }

    return render(request,"pages/site_information.html", context)'''

'''@login_required
def change_address(request):
    site_name = request.POST['site_name']
    contact_email = request.POST['contact_email']
    contact_mobile_number = request.POST['contact_mobile_number']

    map = folium.Map(location=[6.2402, -75.5767], zoom_start=10)
    popup1 = folium.LatLngPopup()
    map.add_child(popup1)
    map = map._repr_html_()
    map = folium.Map(location=[6.2402, -75.5767], zoom_start=10)
    folium.Marker(
        draggable=True
    ).add_to(map)
    map = map._repr_html_()
    context = {
        'map': map,
        'building_name': site_name,
        'building_email': contact_email,
        'building_number': contact_mobile_number,
    }

    return render(request,"pages/site_information.html", context)'''

@login_required
def add_building(request):    
    username = request.user.get_full_name()
    building_information_list = get_building_information(request)
    
    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != '' and request.POST['lat'] != '' and request.POST['lon'] != '' and request.POST['contact_email'] != '':
        building = Building.objects.filter(site_name__iexact=building_information_list[0])
        if building:
            messages.error(request, 'Edificio ya existe')
        else:
            regulation_re = request.POST['sel_regulation']
            lat = request.POST['lat']
            lng = request.POST['lon']
            b = Building.objects.create(site_name=building_information_list[0],full_address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3], regulation=regulation_re, created_by=username, modificated_by=username)
            Address.objects.create(lat=lat, lng=lng, building=b)
            messages.success(request, 'Edificio creado con exito')
    else:
        messages.error(request, 'Por favor llenar todos los campos')
        return render(request, 'pages/site_information.html', 
                      {'building_name': building_information_list[0], 'building_address': building_information_list[1], 
                      'building_email': building_information_list[2],'building_number': building_information_list[3]})
    return render (request, 'pages/site_information.html')

@login_required
def edition_building(request, building_name):
    building = Building.objects.get(site_name=building_name)
    return render(request, "pages/edit_building.html", {'building':building})

@login_required
def edit_building(request, building_name):
    building_information_list = get_building_information(request)

    regulation_req = request.POST['sel_regulation']
    building = Building.objects.get(site_name=building_name)

    if regulation_req != building.regulation:
        building.site_type = None
        messages.error(request, 'Se cambio la normativa: Debe categorizar de nuevo el edificio')

    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != '' and request.POST['contact_email'] != '':
        username = request.user.get_full_name()
        building.site_name = building_information_list[0]
        #building.full_address = building_information_list[1]
        building.contact_email = building_information_list[2]
        building.contact_mobile_number = building_information_list[3]
        building.regulation = regulation_req
        building.modificated_by = username
        building.save()
        messages.success(request, 'Edificio editado con exito')
    else: 
        messages.error(request, 'Por favor llenar todos los campos')
    
    return redirect('/company/search_building')
    
@login_required
def add_building_type(request):
    username = request.user.get_full_name()
    building_information_list = get_building_information(request)
    if request.POST['contact_mobile_number'] != '' and request.POST['site_name'] != ' ' and request.POST['lat'] != '' and request.POST['lon'] != '' and request.POST['contact_email'] != '':
        building = Building.objects.filter(site_name__iexact=building_information_list[0])
        if building:
            messages.error(request, 'Edificio ya existe')
        else:
            regulation_re = request.POST['sel_regulation']

            lat = request.POST['lat']
            lng = request.POST['lon']

            b = Building.objects.create(site_name=building_information_list[0],full_address=building_information_list[1],contact_email=building_information_list[2], contact_mobile_number=building_information_list[3],regulation=regulation_re, created_by=username)
            Address.objects.create(lat=lat, lng=lng, building=b)
            current_question = getQuestions([], b.regulation)
            return render(request,"pages/site_parameterization.html",{'building_name': b.site_name, 'building_regulation': b.regulation, 'current_question':current_question})
    else:
        messages.error(request, 'Por favor llenar todos los campos')
        return render(request, 'pages/site_information.html', 
                      {'building_name': building_information_list[0], 'building_address': building_information_list[1], 
                      'building_email': building_information_list[2],'building_number': building_information_list[3]})
    return render (request, 'pages/site_information.html')

@login_required
def set_building_type(request, building_name, building_type):
    username = request.user.get_full_name()
    building = Building.objects.get(site_name=building_name)
    building.modificated_by=username
    building.site_type = building_type
    building.save()

    messages.success(request, 'Edificio creado con caracterizacion')
    return redirect('/company/search_building')

@login_required
def delete_building(request):
    code_building = request.POST.get('delete_id_item')
    building = Building.objects.get(code=code_building)
    inspections_list = Building.objects.get(site_name=building.site_name).inspection_set.all()

    if len(inspections_list) == 0:
        building.delete()
        messages.success(request, 'Edificio eliminado con exito')
    
    return redirect('/company/search_building')

@login_required
def view_building_information(request, building_name):
    building = Building.objects.get(site_name=building_name)
    inspections = Building.objects.get(site_name=building.site_name).inspection_set.all()

    #print(inspections[1].description)
    descriptions = []
    desc = []
    descs = []
    for i in inspections:
        if i.description != None:
            desc = re.sub("\[|\]","",i.description)
            descs = desc.split("', ")

        for ite,d in enumerate(descs):
            text = re.sub("\'|\.","",d)
            descs[ite] = text

        descriptions.append([i,descs])

    return render(request, "pages/view_building_information.html", {'building':building, 'inspections': inspections, 'descriptions':descriptions})

@login_required
def choose_regulation_to_show(request):
    return render(request, "pages/choose_regulation_to_show.html")

@login_required
def show_regulation_information(request, regulation, is_inspection_question):
    questions = []
    table_list = []
    if is_inspection_question == '0':
        dir = 'apps/company/utilities/choose_type'
        questions = readFileType(dir + '/Group' + regulation + '.txt')

        for ite,q in enumerate(questions):
            if 'img' not in q.image:
                string = q.image
                questions[ite].image = string.split(';')
            else: 
                questions[ite].image = ''
    else:
        dir = 'apps/company/utilities/data_flow'
        questions = readFileIns(dir + '/Flow' + regulation + '.txt')
        #print(questions)

        for ite,q in enumerate(questions):
            if not isinstance(q,Question):
                questions.pop(ite)
        
        for ite,r in enumerate(questions):
            if isinstance(r,Question):
                if 'img' not in r.image and r.image != '[]':
                    string = r.image
                    questions[ite].image = string.split(';')
                else: 
                    questions[ite].image = ''

    return render(request, "pages/show_regulation_information.html", {'questions':questions, 'is_inspection_question':is_inspection_question})

@login_required
def download_inspection_register(request, building_name):
    building = Building.objects.get(site_name=building_name)
    inspections = Inspection.objects.filter(building=building)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="{}.csv'.format(building_name)},
    )

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Direccion', 'Email', 'Numero', 'Caracterizacion', 'Normativa','Creado por', 'Ultima modificacion por'])
    writer.writerow([building.site_name, building.address,building.contact_email,building.contact_mobile_number, building.site_type,
                    building.regulation, building.created_by,building.modificated_by])
    writer.writerow([])
    writer.writerow(['inspector', 'Resultado', 'Descripcion'])

    for i in inspections:
        description = None
        print(i.date)
        if i.description == '[]':
            description = 'Ninguna'
        else:
            description = i.description

        writer.writerow([i.inspected_by, i.is_inspection_successful, description])
        
    return response

@login_required
def law_interface(request):
    return render(request, 'pages/law_interface_select.html')

@login_required
def edit_law(request, law):
    form = ContactForm()
    if 'Group' in law:
        law = law.replace('Group','')
        if request.method == 'POST':
            dic = request.POST.dict()
            if request.POST.get("addOption"):
                form.addOption(dic)
                return render(request, 'pages/law_interface_edit_group.html', {'form': form})
            elif request.POST.get("removeOption"):
                form.removeOption(dic)
                return render(request, 'pages/law_interface_edit_group.html', {'form': form})
            elif request.POST.get("addQuestion"):
                form.addQuestion(dic)
                return render(request, 'pages/law_interface_edit_group.html', {'form': form})
            elif request.POST.get("remove"):
                form.remove(dic)
                return render(request, 'pages/law_interface_edit_group.html', {'form': form})
            else:
                writeFileGroup(law, dic)
                return redirect('/company/')
        else:
            questions = getQuestionsGroup(law)
            form.initials(questions)
            return render(request, 'pages/law_interface_edit_group.html', {'form': form})

    elif 'Flow' in law:
        law = law.replace('Flow','')
        if request.method == 'POST':
            dic = request.POST.dict()
            if request.POST.get("addOption"):
                form.addOption(dic)
                return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
            elif request.POST.get("removeOption"):
                form.removeOption(dic)
                return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
            elif request.POST.get("addQuestion"):
                form.addQuestion(dic)
                return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
            elif request.POST.get("addFlow"):
                form.addFlow(dic)
                return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
            elif request.POST.get("remove"):
                form.remove(dic)
                return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
            else:
                writeFileFlow(law, dic)
                return redirect('/company/')
        else:
            questions = getQuestionsFlow(law)
            form.initials(questions)
    return render(request, 'pages/law_interface_edit_flow.html', {'form': form})
