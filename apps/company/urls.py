from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('site_parameterization',views.site_parameterization, name = "site_parameterization"),
    path('search_building',views.search_building),
    path('search_key/<building_id>',views.search_key),
    path('building_information',views.site_information),
    path('add_building',views.add_building),
    path('add_building_type', views.add_building_type),
    path('set_building_type/<building_id>/<building_type>', views.set_building_type)
]
