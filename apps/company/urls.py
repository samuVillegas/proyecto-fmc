from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('add_building',views.add_building),
    path('search_building',views.search_building)
]