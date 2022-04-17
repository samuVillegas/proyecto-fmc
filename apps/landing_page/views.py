from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .forms import ContactForm, ColorfulContactForm
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

def login(request):
    if request.method == 'POST':
        form = ColorfulContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ColorfulContactForm()
    return render(request, 'pages/law_interface.html', {'form': form})