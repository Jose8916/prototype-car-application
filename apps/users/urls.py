from django.conf.urls import  include
from apps.users.views import *
from apps.users.apiViews import *
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
	path(r'index',login_required(index), name='index'),
	path(r'subscription', subscription, name='subscription'),
	path(r'invoices/', invoices, name='invoices'),
	path(r'invoice/<int:pk>', invoice, name='invoice'),

	path(r'registration', registration, name='registration'),
	# path(r'affiliate-registration/<str:code>',affiliate_registration, name='affiliate-registration'),
	path(r'registration_two',login_required(registration_two), name='registration_two'),

	path(r'categories',login_required(categories), name='categories'),
	path(r'categories/<int:pk>',login_required(categories), name='categories'),
    
	path(r'subscription2',login_required(subscription2), name='subscription2'),
	path(r'subscription2/<int:pk>',login_required(subscription2), name='subscription2'),

	path(r'coupons',login_required(coupons), name='coupons'),
	path(r'coupons/<int:pk>',login_required(coupons), name='coupons'),
	
	path(r'users',login_required(users), name='users'),
	path(r'users/<int:pk>',login_required(users), name='users'),

	path(r'operational_users',login_required(operational_users), name='operational_users'),
	path(r'operational_users/<int:pk>',login_required(operational_users), name='operational_users'),
	
	path(r'print_cards',login_required(print_cards), name='print_cards'),
	path(r'print_cards/<int:pk>',login_required(print_cards), name='print_cards'),
 
 	path(r'allys',login_required(allys), name='allys'),
	path(r'allys/<int:pk>',login_required(allys), name='allys'),
 	path(r'allys_two',login_required(allys_two), name='allys_two'),

	path(r'activate-card',login_required(activate_card), name='activate-card'),
	#api codigos
	path(r'api_cod/<str:cod>', api_cod, name='api_cod'),
	path(r'api_events_wompi', api_events_wompi, name='api_events_wompi'),
	path(r'login/', login_user, name='login'),
 	
    path(r'logout/', logout_user, name='logout'),
    path(r'password_recovery/', password_recovery, name='password_recovery'),
    path(r'password_reset/<uidb64>/<token>/', password_reset, name='password_reset'),
    path(r'profile_front', profile_front, name='profile_front'),

    path(r'activate_cards', activate_cards, name='activate_cards'),
    path(r'activate_card/<int:pk>', activate_card, name='activate_card'),
]