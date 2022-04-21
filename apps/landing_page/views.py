from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .forms import ContactForm
import logging
# Create your views here.

def langing_page(request):
    return render(request,"pages/index_landing_page.html")

def law_interface(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email)
    if email and password:
        if user and check_password(password,user[0].password):
            if user[0].is_superuser:
                print('Admin')
                return redirect('/company/')
            else: 
                print('Employee')
        else:
            messages.error(request,'No existen usuarios con esas credenciales')  
    return render(request,"pages/login.html")

from apps.company.utilities.data_flow.DataFlow import getQuestions2, writeFile
def login(request):
    if request.method == 'POST':
        writeFile('NSR10', request.POST.dict())
        return redirect('/company/')
    else:
        questions = getQuestions2('NSR10')
        form = ContactForm()
        form.initials(questions)
    return render(request, 'pages/law_interface.html', {'form': form})