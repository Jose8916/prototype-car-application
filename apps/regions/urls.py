from django.conf.urls import  include
from apps.regions.views import *
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path(r'countries',login_required(countries), name='countries'),
	path(r'countries/<int:pk>',login_required(countries), name='countries'),
	path(r'departments',login_required(departments), name='departments'),
	path(r'departments/<int:pk>',login_required(departments), name='departments'),
	path(r'cities',login_required(cities), name='cities'),
	path(r'cities/<int:pk>',login_required(cities), name='cities'),
	path(r'locations_front', locations_front, name='locations_front'),
	path(r'locations_front/<int:pk>', locations_front, name='locations_front')
]