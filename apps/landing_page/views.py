from django.shortcuts import render, redirect
# Create your views here.

def langing_page(request):
    return render(request,"pages/index_landing_page.html")

def login(request):
    return render(request,"pages/login.html")


