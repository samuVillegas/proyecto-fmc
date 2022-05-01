from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.data_flow.DataFlow import getQuestions as getQuestionsInsp
# Create your views here.

def langing_page(request):
    return render(request,"pages/index_landing_page.html")

def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email)
    if email and password:
        if user and check_password(password,user[0].password):
            if user[0].is_superuser:
                print('Admin')
                return redirect('/administration/')
            else: 
                print('Employee')
                return redirect('/company/')
        else:
            messages.error(request,'No existen usuarios con esas credenciales')  
    return render(request,"pages/login.html")

def inspect(request):
    return render(request,"pages/choose_regulation.html")

def parameterization(request, building_regulation):
    current_question = getQuestions([], building_regulation)
    return render(request,"pages/site_parameterization_no_loging.html", {'building_regulation': building_regulation, 'current_question':current_question})

def search_key_no_loging(request, building_regulation):
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

    return render(request,"pages/site_parameterization_no_loging.html",{'current_question':current_question,'building_regulation': building_regulation, "is_material_list": is_material_list})

def inspection(request, building_type,building_regulation):
    current_question = getQuestionsInsp([], building_regulation, building_type)
    return render(request,"pages/site_inspection_no_loging.html", {'building_regulation': building_regulation, 'current_question':current_question, 'building_type':building_type})

def search_flow_no_loging(request, building_type, building_regulation):
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
    return render(request,"pages/site_inspection_no_loging.html",{'current_question':current_question, 'building_regulation': building_regulation,"building_type": building_type, 'is_material_list': is_material_list})