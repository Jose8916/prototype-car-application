from django.shortcuts import render,redirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q, Subquery, OuterRef
from urllib.parse import urlencode
from apps.vehicles.models import *
from apps.vehicles.forms import *

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def registration_vehicles(request, pk=None):
	subquery=Card.objects.filter(user=OuterRef('user_id'))
	extended_users = Extended_User.objects.filter(user__groups__id = 2).annotate(code_card=Subquery(subquery.values('code')[:1]))
	context={
		'active_registration_vehicles':'text-dark',
	}
	if request.GET.get('document') != None and request.GET.get('code') != None:
		try:
			extended_user = extended_users.get(document_number= request.GET.get('document'), code_card=request.GET.get('code'))
			context['extended_user'] = extended_user
		except Exception as e:
			print(e)
			context['error'] = "El usuario no es un conductor o los datos ingresados estan incorrectos"

		vehicles= Vehicle.objects.filter(user_id=extended_user.user.id)
		context['vehicles'] = vehicles
		if pk:
			vehicle = vehicles.get(id=pk)
			context['modal'] = 'show'
			context['pk'] = pk
		if request.POST:
			request.POST = request.POST.copy()
			request.POST.update({'editing_user': request.user.id, 'user': extended_user, 'state': 2})
			form = VehicleForm(request.POST, request.FILES,instance=vehicle) if pk else VehicleForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()

				#se crea una url con los datos opcionales
				base_url = reverse('vehicles:registration_vehicles')  # 1 /products/
				query_string =  urlencode({'document': request.GET.get('document'), "code": request.GET.get('code')})  # 2 category=42
				url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
				return redirect(url)
			else:
				print(form.errors)
				context['modal'] = 'show'
		else:
			#se parsea las fechas desde aqui para no hacerlo desde el template eso ayuda cuando haya un error tengan el mismo formato
			form = VehicleForm(instance=vehicle, initial={ "soat_date": vehicle.soat_date.strftime('%Y-%m-%d'), "technomechanical_date": vehicle.technomechanical_date.strftime('%Y-%m-%d')}) if pk else None
		context['form'] = form
	return render(request, "vehicles/registration_vehicles.html", context)


def vehicles_front(request, pk= None):
	vehicles = Vehicle.objects.filter(user__user_id= request.user.id)
	card = Card.objects.get(user__user_id=request.user.id)
	states= State.objects.all()
	context={
		'vehicles': vehicles,
		"card": card,
		"states": states
	}
	form = None
	if pk:
		context['modal'] = 'show'
		context['pk'] = pk
	if request.method == 'POST':
		vehicle = Vehicle.objects.get(pk=request.POST['vehicle_id_input'])
		vehicle.state_id = request.POST['state']
		vehicle.use_condition = request.POST['use_condition']
		Vehicle.objects.exclude(pk=request.POST['vehicle_id_input']).update(use_condition='Libre')
		vehicle.save()
		# form = VehicleForm(request.POST)
		# if form.is_valid():
		# 	return redirect('vehicles:vehicles_front')
		# else:
		# 	print(form.errors)
		# 	context['modal'] = 'show'
	else:
		print(vehicles)
	context['form'] = form
	return render (request, "vehicles/vehicles_front.html", context)

def vehicles_list(request, pk=None):

	vehicles = Vehicle.objects.all().order_by("id")
	cities = City.objects.all()
	page = request.GET.get("page", 1)
	paginator = Paginator(vehicles, 5)
	bar_search= request.GET.get('bar_search', "")
	city_search= request.GET.get("city_search", "")
	try:
		vehicles_list = paginator.page(page)
	except PageNotAnInteger:
		vehicles_list = paginator.page(1)
	except EmptyPage:
		vehicles_list = paginator.page(paginator.num_pages)

	if bar_search != "":
		vehicles_list = Vehicle.objects.filter(Q(plate__icontains = bar_search)|Q(user__contact_person_phone__icontains = bar_search)|Q(brand__icontains = bar_search))
	if city_search != "":
		vehicles_list = Vehicle.objects.filter(user__city=city_search)

	context={
		'active_vehicles': 'text-dark',
		'vehicles': vehicles,
		'cities': cities,
		'name': 'Vehiculos',
		"vehicles_list": vehicles_list
	}

	if pk:
		vehicles_list = vehicles.get(id=pk)
		context['modal'] = 'show'
		context['publication'] = vehicles_list
		if request.POST:
			form=VehicleForm(request.POST, request.FILES, instance=vehicles_list)
			if form.is_valid():
				obj_vehicle = form.save(commit=False)
				obj_vehicle.modification_date = timezone.now()
				obj_vehicle.save()
				return redirect('vehicles:vehicles_list')
			else:
				context['form'] = form


	if request.POST:
		request.POST = request.POST.copy()
		request.POST.update({"route": "vehicles_list"})
		form = VehicleForm(request.POST,request.FILES, instance=vehicles_list) if pk else VehicleForm(request.POST,request.FILES)
		if form.is_valid():
			obj_vehicle= form.save(commit=False)
			obj_vehicle.create_date = timezone.now()
			invitation_code = form.cleaned_data.get("invitation_code")
			if invitation_code:
				obj_card = Card.objects.filter(code=invitation_code).first()
				obj_user = obj_card.user
				obj_vehicle.user = obj_user			
			obj_vehicle.save()
			return redirect('vehicles:vehicles_list')
		else:
			context['modal'] = 'show'
	else:
		form = VehicleForm(instance=vehicles_list) if pk else VehicleForm()
	context['form'] = form

	return render (request, "vehicles/vehicles_list.html", context)
