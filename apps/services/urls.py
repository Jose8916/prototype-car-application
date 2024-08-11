from django.conf.urls import  include
from apps.services.views import *
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path(r'pqr',login_required(pqr), name='pqr'),
	path(r'pqr/<int:pk>',login_required(pqr), name='pqr'),
	path(r'pqr_front',login_required(pqr_front), name='pqr_front'),
	path(r'publications',login_required(publications), name='publications'),
	path(r'publications/<int:pk>',login_required(publications), name='publications'),
	path(r'service',login_required(service), name='service'),
 	path(r'travel_history_back',login_required(travel_history_back), name='travel_history_back'),
	path(r'service/<int:pk>',login_required(service), name='service'),
	path(r'service_begin',login_required(service_begin), name='service_begin'),
	path(r'service_front_associate', service_front_associate, name='service_front_associate'),
	path(r'service_front_associate_2/<int:pk>', service_front_associate_2, name='service_front_associate_2'),
	path(r'service_front_associate_3/<int:pk>', service_front_associate_3, name='service_front_associate_3'),
	path(r'service_front_associate_4/<int:pk>', service_front_associate_4, name='service_front_associate_4'),
	path(r'service_front_affiliate', login_required(service_front_affiliate), name='service_front_affiliate'),
	path(r'travel_history',login_required(travel_history), name='travel_history'),

]