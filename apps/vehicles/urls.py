from django.conf.urls import  include
from apps.vehicles.views import *
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
	path(r'registration_vehicles', login_required(registration_vehicles), name='registration_vehicles'),
	path(r'registration_vehicles/<int:pk>', login_required(registration_vehicles), name='registration_vehicles'),
	path('vehicles_front',login_required(vehicles_front), name='vehicles_front'),
	path(r'vehicles_list', login_required(vehicles_list), name='vehicles_list'),
	path(r'vehicles_list/<int:pk>', login_required(vehicles_list), name='vehicles_list'),
]