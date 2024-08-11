from django.shortcuts import render,redirect
from apps.regions.models import *
from apps.users.models import *
from apps.regions.forms import *
from django.db.models import Q

# Create your views here.
def countries(request,pk=None):
	countries=Country.objects.all().order_by("name").exclude(state="3")
	states=State.objects.all().order_by("name").exclude(name="Eliminado")
	context={
		'active_countries':'text-dark',
		'countries':countries,
		'states':states,
	}
	if pk:
		country = Country.objects.get(id=pk)
		context['modal'] = 'show'
		context['country'] = country
		if request.POST.get('action') == 'create':
			form=CountryForm(request.POST, instance=country)
			if form.is_valid():
				form.save()
				return redirect('regions:countries')
			else:
				context['form'] = form
				context['modal'] = 'show'
	else :
		if request.POST.get('action') == 'create':
			form = CountryForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('regions:countries')
			else:
				context['form'] = form
				context['modal'] = 'show'
		elif request.POST.get('action') == 'delete':
			intsance = countries.get(pk=request.POST['deletepost'])
			intsance.state_id=3
			intsance.save()
			return redirect('regions:countries')
	return render(request, "regions/countries.html", context)

def departments(request,pk=None):
	departments=Department.objects.all().order_by("name").exclude(
		Q(state="3")|
		Q(country__state=2)|
		Q(country__state=3)
	)
	states=State.objects.all().order_by("name")
	context={
		'active_departments':'text-dark',
		'departments':departments,
		'states':states,
	}
	if pk:
		department = departments.get(id=pk)
		context['modal'] = 'show'
		context['department'] = department
	if request.POST:
		request.POST = request.POST.copy()
		# se asigan por defecto colombia
		request.POST.update({'country': 1 })
		form =  DepartmentForm(request.POST, instance=department) if pk else DepartmentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('regions:departments')
		else:
			context['form'] = form
			context['modal'] = 'show'
	return render(request, "regions/departments.html",context)

def cities(request, pk=None):
	cities=City.objects.all().order_by("name").exclude(Q(state=3)|Q(department__state=2)|Q(department__state=3)|Q(department__country__state=2)|Q(department__country__state=3)).order_by('cod')
	departments=Department.objects.all().order_by("name").exclude(Q(state="3")|Q(country__state=2)|Q(country__state=3)
	)
	states=State.objects.all().order_by("name")
	context={
		'active_cities':'text-dark',
		'cities':cities,
		'departments':departments,
		'states':states,
	}
	if pk:
		city = cities.get(id=pk)
		context['modal'] = 'show'
		context['city'] = city
	if request.POST:
		# request.POST = request.POST.copy()
		# request.POST.update({'country': 1 })
		form =  CityForm(request.POST, instance=city) if pk else CityForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('regions:cities')
		else:
			print(form.errors)
			context['form'] = form
			context['modal'] = 'show'
	return render(request, "regions/cities.html",context)

def locations_front(request, pk=None):
	locations=Location.objects.filter(user=request.user, state=1, city__state = 1 , city__department__state=1, city__department__country__state=1);
	cities= City.objects.filter(state=1, department__state=1, department__country__state=1)
	extended_user=Extended_User.objects.get(user_id= request.user.id)
	card= Card.objects.filter(user_id=request.user.id)[:1]
	context={
		"locations":locations,
		"extended_user":extended_user,
		"card":card,
		"cities": cities,	
	}

	if pk and request.GET.get('delete')!= None:
		location = locations.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk
		context['delete'] = True 
	elif pk:
		location = locations.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk
	if request.POST:
		updated_request = request.POST.copy()
		state_location = 2 if request.GET.get('delete') != None and pk else 1
		updated_request.update({'user': request.user.id, 'state': state_location, 'delete': request.GET.get('delete')
			})
		form= LocationForm(updated_request, instance=location) if pk else LocationForm(updated_request)
		if form.is_valid():
			form.save()
			return redirect('regions:locations_front')
		else:
			print(form.errors)
			context['modal'] = 'show'
	else:
		form = LocationForm(instance=location) if pk else None
	context['form'] = form
	return render(request, "regions/locations_front.html",context)	