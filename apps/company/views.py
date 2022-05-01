from cgi import print_directory
from typing import final
from django.shortcuts import render, redirect
from django.contrib import messages
import re
import os

from matplotlib import image
from numpy import append

from .models import Building, Inspection
from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.data_flow.DataFlow import getQuestions as getQuestionsInsp
from apps.company.utilities.input_request import get_building_information
from apps.company.utilities.choose_type.Group import readFile as readFileType
from apps.company.utilities.data_flow.DataFlow import readFile as readFileIns
from apps.company.utilities.data_flow.Question import Question
from apps.company.utilities.forms import ContactForm
from apps.company.utilities.data_flow.DataFlow import getQuestionsFlow, writeFileFlow
from apps.company.utilities.choose_type.Group import getQuestionsGroup, writeFileGroup

def index(request):
    return render(request,"pages/index.html")

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

def site_inspection(request, building_name, building_type, building_regulation, building_id):
    building = Building.objects.get(code=building_id)
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
    return render(request, "pages/site_inspection.html", {'current_question':current_question, 'building_id': building_id, 'building_name': building_name, 'building_type': building_type, 'building_regulation': building_regulation, 'is_material_list':is_material_list})

def site_parameterization_from_edit(request, building_id, building_name, building_regulation):
    current_question = getQuestions([], building_regulation)
    is_material_list = False
    return render(request,"pages/site_parameterization.html", {'current_question':current_question , 'building_id':building_id,
                    'building_name': building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

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

def search_key(request, building_id, building_name, building_regulation):
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

    return render(request,"pages/site_parameterization.html",{'current_question':current_question, 'building_id':building_id, 'building_name':building_name, 'building_regulation': building_regulation, "is_material_list": is_material_list})

def search_flow(request, building_id, building_name, building_type, building_regulation):
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
    return render(request,"pages/site_inspection.html",{'current_question':current_question, 'building_regulation': building_regulation, 'building_id':building_id, 'building_name':building_name, "building_type": building_type, 'is_material_list': is_material_list})

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
    b = Building.objects.filter(site_name__iexact=building_name).get()
    Inspection.objects.create(description=final_flow, is_inspection_successful=is_inspection_succesfull, building=b)
    return redirect('/company/search_building')

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
    inspections_list = Building.objects.get(site_name=building.site_name).inspection_set.all()

    if len(inspections_list) == 0:
        building.delete()
        messages.success(request, 'Edificio eliminado con exito')
    
    return redirect('/company/search_building')

def view_building_information(request, building_id):
    building = Building.objects.get(code=building_id)
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

def choose_regulation_to_show(request):
    return render(request, "pages/choose_regulation_to_show.html")

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

def law_interface(request):
    return render(request, 'pages/law_interface_select.html')

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
