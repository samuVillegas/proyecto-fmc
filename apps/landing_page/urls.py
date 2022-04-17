from django.urls import path
from . import views


urlpatterns = [
    path('',views.langing_page),
    path('login',views.login),
    path('law_interface', views.law_interface), 
]
