from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home(request):
    return render(request, 'home.html', {'name': 'Pablo Maya'})
    #return HttpResponse('<h1>Welcome to home page!</h1>')

