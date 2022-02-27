from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('site_parameterization',views.site_parameterization),
    path('search_building',views.search_building),
    path('search_key',views.search_key),
    path('building_information',views.site_information)
]