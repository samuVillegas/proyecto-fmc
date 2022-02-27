from django.shortcuts import render, redirect
from apps.company.utilities.choose_type.Group import getQuestions

# Create your views here
def index(request):
    return render(request,"pages/index.html",{'message':'Hola mundo'})

def add_building(request): 
    current_question = getQuestions([])
    return render(request,"pages/add_building.html",{'current_question':current_question})
    
def search_building(request): 
    return render(request,"pages/search_building.html")

def search_key(request):
    current_ids = request.POST.get('current_ids')
    split_current_ids = current_ids.split(',')
    current_question = getQuestions(split_current_ids)
    return render(request,"pages/add_building.html",{'current_question':current_question})
    