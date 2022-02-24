from django.shortcuts import render, redirect

# Create your views here
def index(request):
    return render(request,"pages/index.html",{'message':'Hola mundo'})

def add_building(request): 
    return render(request,"pages/add_building.html")
    
def search_building(request): 
    return render(request,"pages/search_building.html")
