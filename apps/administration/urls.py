from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('inspectors/',views.inspectors),
    path('buildings/',views.buildings),
    path('regulations/',views.regulations),
    path('map_building/', views.map_building),
]
