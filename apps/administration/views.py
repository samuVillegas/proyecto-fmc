from django.shortcuts import render
from sklearn import inspection
from apps.company.models import Building, Address, Inspection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from apps.company.utilities.choose_type.Group import getQuestions
from apps.company.utilities.data_flow.DataFlow import getQuestions as getQuestionsInsp
from apps.company.utilities.input_request import get_building_information
from apps.company.utilities.choose_type.Group import readFile as readFileType
from apps.company.utilities.data_flow.DataFlow import readFile as readFileIns
from apps.company.utilities.data_flow.Question import Question
from apps.company.utilities.forms import ContactForm
from apps.company.utilities.data_flow.DataFlow import getQuestionsFlow, writeFileFlow
from apps.company.utilities.choose_type.Group import getQuestionsGroup, writeFileGroup
# Create your views here.

@login_required
def index(request):
    return render(request,"pages/index_admin.html")

@login_required
def map_building(request):
    address_list = Address.objects.all()
    data = []
    is_inspection_successful = None
    for addr in address_list:
        inspection_list = Building.objects.get(site_name=addr.building.site_name).inspection_set.all()
        if(len(inspection_list) > 0):
            is_inspection_successful = inspection_list[len(inspection_list) - 1].is_inspection_successful
        data.append({
            "lat":addr.lat,"lng":addr.lng, 
            "is_inspection_successful": is_inspection_successful,
            "site_name":addr.building.site_name, "site_type": addr.building.site_type
            })

    return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")

@login_required
def show_map(request):
    return render(request,"pages/map.html")

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
def choose_regulation_to_show_admin(request):
    return render(request, "pages/choose_regulation_to_show_admin.html")

@login_required
def show_regulation_information_admin(request, regulation, is_inspection_question):
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

    return render(request, "pages/show_regulation_information_admin.html", {'questions':questions, 'is_inspection_question':is_inspection_question})

@login_required
def law_interface_admin(request):
    return render(request, 'pages/law_interface_select_admin.html')

@login_required
def edit_law_admin(request, law):
    form = ContactForm()
    if 'Group' in law:
        law = law.replace('Group','')
        if request.method == 'POST':
            dic = request.POST.dict()
            if request.POST.get("addOption"):
                form.addOption(dic)
                return render(request, 'pages/law_interface_edit_group_admin.html', {'form': form})
            elif request.POST.get("removeOption"):
                form.removeOption(dic)
                return render(request, 'pages/law_interface_edit_group_admin.html', {'form': form})
            elif request.POST.get("addQuestion"):
                form.addQuestion(dic)
                return render(request, 'pages/law_interface_edit_group_admin.html', {'form': form})
            elif request.POST.get("remove"):
                form.remove(dic)
                return render(request, 'pages/law_interface_edit_group_admin.html', {'form': form})
            else:
                writeFileGroup(law, dic)
                return redirect('/administration/')
        else:
            questions = getQuestionsGroup(law)
            form.initials(questions)
            return render(request, 'pages/law_interface_edit_group_admin.html', {'form': form})

    elif 'Flow' in law:
        law = law.replace('Flow','')
        if request.method == 'POST':
            dic = request.POST.dict()
            if request.POST.get("addOption"):
                form.addOption(dic)
                return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
            elif request.POST.get("removeOption"):
                form.removeOption(dic)
                return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
            elif request.POST.get("addQuestion"):
                form.addQuestion(dic)
                return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
            elif request.POST.get("addFlow"):
                form.addFlow(dic)
                return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
            elif request.POST.get("remove"):
                form.remove(dic)
                return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
            else:
                writeFileFlow(law, dic)
                return redirect('/administration/')
        else:
            questions = getQuestionsFlow(law)
            form.initials(questions)
    return render(request, 'pages/law_interface_edit_flow_admin.html', {'form': form})
