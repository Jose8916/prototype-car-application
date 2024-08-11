from django.conf.urls import  include
from apps.taxes.views import *
from django.urls import path
from django.contrib.auth.decorators import login_required
# èsto hace que saque horas aleatorias se deja por si a futuro toca implentarlo
# initial_benefits_policy()
urlpatterns = [
	path(r'membership',login_required(membership), name='membership'),
	path(r'agreement',login_required(agreement), name='agreement'),
	path(r'collections',login_required(collections), name='collections'),
	path(r'collections/<int:pk>',login_required(collections), name='collections'),
	path(r'time_zone',login_required(time_zone), name='time_zone'),
	path(r'time_zone/<int:pk>',login_required(time_zone), name='time_zone'),
	path(r'rate',login_required(rate), name='rate')
	# path(r'units_range',login_required(units_range), name='units_range'),
]