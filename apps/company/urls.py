from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    #path('site_parameterization',views.site_parameterization, name = "site_parameterization"),
    path('search_building',views.search_building),
    path('search_key/<building_id>/<building_name>/<building_regulation>',views.search_key),
    path('building_information',views.site_information),
    path('add_building',views.add_building),
    path('add_building_type', views.add_building_type),
    path('set_building_type/<building_id>/<building_type>', views.set_building_type),
    path('edit_building/<building_id>', views.edit_building),
    path('edition_building/<building_id>', views.edition_building),
    path('site_parameterization_from_edit/<building_id>/<building_name>/<building_regulation>',views.site_parameterization_from_edit),
    path('delete_building', views.delete_building),
    path('view_building_information/<building_id>', views.view_building_information),
    path('site_national_inspection/<building_name>/<building_type>/<building_id>', views.site_national_inspection),
    path('choose_regulation/<building_name>/<building_type>/<building_id>', views.choose_regulation),
    path('search_flow/<building_id>/<building_name>/<building_type>', views.search_flow),
    path('law_interface', views.law_interface), 
    path('edit_group_law', views.edit_group_law), 
    path('edit_flow_law', views.edit_flow_law), 
    path('edit_group_law1', views.edit_group_law1), 
    path('edit_flow_law1', views.edit_flow_law1), 
]
