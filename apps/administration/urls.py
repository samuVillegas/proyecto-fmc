from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('inspectors/',views.inspectors),
    path('buildings/',views.buildings),
    path('choose_regulation_to_show/', views.choose_regulation_to_show_admin),
    path('show_regulation_information/<regulation>/<is_inspection_question>', views.show_regulation_information_admin),
    path('law_interface', views.law_interface_admin), 
    path('edit_law/<law>', views.edit_law_admin), 
    #Peticiones para el dashboard
    path('dashboard_char_regulation/',views.dashboard_char_regulation),
    path('dashboard_buildings_by_type/',views.dashboard_buildings_by_type),
    path('dashboard_building_inspection_state/',views.dashboard_building_inspection_state)
]
