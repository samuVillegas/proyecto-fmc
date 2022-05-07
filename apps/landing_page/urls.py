from django.urls import path
from . import views


urlpatterns = [
    path('',views.langing_page),
    path('login',views.login, name="login"),
    path('inspect',views.inspect),
    path('parameterization/<building_regulation>', views.parameterization),
    path('search_key_no_loging/<building_regulation>', views.search_key_no_loging),
    path('inspection/<building_type>/<building_regulation>', views.inspection),
    path('search_flow_no_loging/<building_type>/<building_regulation>', views.search_flow_no_loging),
]
