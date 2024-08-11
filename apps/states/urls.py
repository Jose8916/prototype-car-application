from django.conf.urls import  include
from apps.states.views import *
from django.urls import path


urlpatterns = [
	path(r'glamper/',glamper, name='glamper'),
	path(r'header_prueba/',header_prueba, name='header_prueba'),
]