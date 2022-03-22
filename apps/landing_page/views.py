from django.shortcuts import render, redirect
# Create your views here.

def langing_page(request):
    return render(request,"containers/base_landing_page.html")
