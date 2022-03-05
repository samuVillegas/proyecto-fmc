from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('site_parameterization',views.site_parameterization, name = "site_parameterization"),
    path('search_building',views.search_building),
    path('search_key/<building_id>/<building_name>',views.search_key),
    path('building_information',views.site_information),
    path('add_building',views.add_building),
    path('add_building_type', views.add_building_type),
    path('set_building_type/<building_id>/<building_type>', views.set_building_type),
    path('edit_building/<building_id>', views.edit_building),
    path('edition_building/<building_id>', views.edition_building),
    path('site_parameterization_from_edit/<building_id>/<building_name>',views.site_parameterization_from_edit),
    path('delete_building/<building_id>', views.delete_building),
    path('view_building_information/<building_id>', views.view_building_information),
]
