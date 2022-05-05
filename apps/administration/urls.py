from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('inspectors/',views.inspectors),
    path('buildings/',views.buildings),
    path('regulations/',views.regulations),
    #Peticiones para el dashboard
    path('dashboard_char_regulation/',views.dashboard_char_regulation),
    path('dashboard_buildings_by_type/',views.dashboard_buildings_by_type),
    path('dashboard_building_inspection_state/',views.dashboard_building_inspection_state)
]
