from django.shortcuts import render,redirect
from django.utils import timezone
from django.http import QueryDict
from django.db.models import F, Q, Sum, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import json

from apps.services.models import *
from apps.services.forms import *
from apps.states.models import *
from apps.vehicles.models import *
# Create your views here.
def pqr(request, pk= None):
	pqrs = Pqr.objects.filter(service__isnull= True).order_by("-modification_date")
	type_pqrs=TypePqr.objects.all()
	states=State_Pqr.objects.all()
	pqr=None
	bar_search= request.GET.get('bar_search', "")
	filter_state= request.GET.get("filter_state", "")
	context={
		'type_pqrs': type_pqrs,
		'states': states,
		'active_pqr':'text-dark',
		'name': 'Pqr'
	}
	if pk:
		pqr=pqrs.get(id=pk)
		context['modal'] = 'show'
		context['pqr'] = pqr
	if bar_search != "":
		pqrs= pqrs.filter(Q(user_question__document_number__icontains = bar_search)|Q(user_question__cell_phone__icontains = bar_search)|Q(user_question__phone_secondary__icontains = bar_search))
	if filter_state != "":
		pqrs= pqrs.filter(state_id=filter_state)
	context['pqrs']=pqrs

	if request.POST:
		updated_request = request.POST.copy()
		if pqr:
			updated_request.update({'user_answer': request.user.id, 'modification_date': timezone.now(), "route": "pqr_edit"})
			form=PqrForm(updated_request, instance=pqr)
		else:
			updated_request.update({'user_question': request.user.id, 'state': 1, 'modification_date': timezone.now(), "route": "pqr"})
			form=PqrForm(updated_request)
		if form.is_valid():
			form.save()
			return redirect('services:pqr')
		else:
			context['form'] = form
			context['modal'] = 'show'
			print(form.errors)

	page = request.GET.get('page', 1)
	paginator = Paginator(pqrs,20)
	try:
		pqrs = paginator.page(page)
	except PageNotAnInteger:
		pqrs = paginator.page(1)
	except EmptyPage:
		pqrs = paginator.page(paginator.num_pages)
	context['pqrs']= pqrs

	return render (request, "services/pqr.html", context)

def pqr_front(request):
	pqrs = Pqr.objects.filter(user_question_id= request.user.id, service__isnull= True).order_by("-modification_date")
	type_pqrs=TypePqr.objects.all()
	extended_user=Extended_User.objects.get(user_id= request.user.id)
	card= Card.objects.filter(user_id=request.user.id)[:1]
	context={
		'pqrs': pqrs,
		'type_pqrs': type_pqrs,
		"extended_user":extended_user,
		"card":card,
	}
	if request.method== 'POST':
		updated_request = request.POST.copy()
		updated_request.update({'user_question': request.user.id, 'modification_date': timezone.now(), 'creation_date': timezone.now(), 'state':1, "route": "pqr_front_create"})
		form= PqrForm(updated_request)
		if form.is_valid():
			form.save()
			return redirect('services:pqr_front')
		else:
			print(form.errors)
			context['modal'] = 'show'
	else:
		form = PqrForm()
		
	context['form'] = form
	print(request.POST)
	return render (request, "services/pqr_front.html", context)

def publications(request, pk=None):
	publications = Publication.objects.all() 
	states = State.objects.all()
	context={
		'active_publications': 'text-dark',
		'states': states,
		'publications': publications
	}
	if pk:
		publication = publications.get(id=pk)
		context['modal'] = 'show'
		context['publication'] = publication
		if request.POST:
			form=PublicationForm(request.POST, request.FILES, instance=publication)
			if form.is_valid():
				form.save()
				return redirect('services:publications')
			else:
				context['form'] = form
	else:
		if request.POST:
			form=PublicationForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return redirect('services:publications')
			else:
				print(form.errors)
				context['form'] = form
				context['modal'] = 'show'
	return render (request, "services/publications.html", context)

def service(request, pk= None):
	collections= Collection.objects.filter(state_id=1)
	type_pqrs=TypePqr.objects.all()
	cities=City.objects.all()
	states=State_Pqr.objects.all()
	states_service= StateService.objects.all()
	subquery= Card.objects.filter(user_id=OuterRef('user_receiving')).values('code')
	subquery1= Card.objects.filter(user_id=OuterRef('user_providing')).values('code')
	services = Service.objects.all().prefetch_related(models.Prefetch('pqr_set', queryset=Pqr.objects.select_related('service'),  to_attr='pqr_records'), models.Prefetch('servicecollection_set', queryset=ServiceCollection.objects.select_related('service'),  to_attr='service_collection_records')).annotate(cod_receiving= Subquery(subquery[:1]), cod_providing= Subquery(subquery1[:1]) ).order_by("-creation_date")
	bar_search= request.GET.get('bar_search', "")
	city_search= request.GET.get('city_search', "")
	filter_state= request.GET.get("filter_state", "")
	
	context={
		'collections': collections,
		'type_pqrs': type_pqrs,
		'cities': cities,
		'states': states,
		'states_service': states_service,
		'active_service':'text-dark',
		'name': 'Servicio'
	}
	if pk:
		service= services.get(id=pk)
		context['service'] = service
		pqr= None
		if bool(service.pqr_records):
			pqr = service.pqr_records[0]
			context['pqr'] = pqr
		context['modal'] = 'show'

	if bar_search != "":
		services= services.filter(Q(user_receiving__document_number__icontains = bar_search)|Q(user_receiving__cell_phone__icontains = bar_search)|Q(user_receiving__phone_secondary__icontains = bar_search)|Q(user_providing__document_number__icontains = bar_search)|Q(user_providing__cell_phone__icontains = bar_search)|Q(user_providing__phone_secondary__icontains = bar_search)|Q(cod_receiving__icontains = bar_search)|Q(cod_providing__icontains = bar_search))
	if filter_state != "":
		services= services.filter(state_id=filter_state)
	if city_search != "":
		services= services.filter(location__city_id=city_search)

	context['services'] = services
	if request.POST:
		updated_request = request.POST.copy()
		if pqr:
			updated_request.update({'user_answer': request.user.id, 'modification_date': timezone.now(), "route": "service_edit"})
			form = PqrForm(updated_request, instance=pqr)
			if form.is_valid():
				form.save()
				return redirect('services:service')
			else:
				print(form.errors)
				context['form'] = form
		else:
			updated_request.update({'service': service.id, 'user_answer': request.user.id, 'modification_date': timezone.now(), "route": "service"})
			form = PqrForm(updated_request)
			form_service = ServiceForm(updated_request, instance=service)
			if  form.is_valid() and form_service.is_valid():
				form.save()
				form_service.save()
				return redirect('services:service')
			else:
				print(form.errors)
				print(form_service.errors)
				context['form'] = form
				context['form_service'] = form_service

	page = request.GET.get('page', 1)
	paginator = Paginator(services,20)
	try:
		services = paginator.page(page)
	except PageNotAnInteger:
		services = paginator.page(1)
	except EmptyPage:
		services = paginator.page(paginator.num_pages)
	context['services']= services

	return render (request,"services/service.html",context)

def service_begin(request):
	context={
	}
	return render (request,"services/service_begin.html",context)

def service_front_associate(request):
	publications_secondary=Publication.objects.filter(state=1)
	extended_user=Extended_User.objects.get(user_id= request.user.id)
	card= Card.objects.filter(user_id=request.user.id)[:1]
	vehicle= Vehicle.objects.filter(user_id=request.user.id)
	publications_secondary = [publications_secondary[x:x+2] for x in range(0, len(publications_secondary), 2)]
	context={
	"publications_secondary": publications_secondary,
	"extended_user":extended_user,
	"card":card,
	"vehicle": vehicle,
	}
	if request.POST:
		try:
			vehicle= Vehicle.objects.get(user__user_id= request.user.id, state_id=1)
			print(vehicle)
			try:
				service= Service.objects.get(state=1, code= request.POST['code_verify'])
				service.state_id=2
				service.vehicle_id= vehicle.id
				service.time_start= timezone.now()
				service.save()
				return redirect('services:service_front_associate_2', pk=service.id)
			except Exception as e:
				print(e)
				context['error'] = "* El Servicio no existe"
		except Exception as e:
			print(e)
			context['error'] = "* Escoge un vehiculo para prestar el servicio"
	return render (request,"services/service_front_associate.html",context)

def service_front_associate_2(request, pk):
	# , associate_id= request.user.id
	service= Service.objects.get(id=pk, state_id=2)
	card= Card.objects.filter(user_id=service.user_receiving.user.id)[:1]
	context= {
	 "service": service,
	 "card": card
	}
	if request.POST:
		service.time_stop=timezone.now()
		service.save()
		return redirect('services:service_front_associate_3', pk=service.id)
	return render (request,"services/service_front_associate_2.html",context)

def service_front_associate_3(request, pk):
	service= Service.objects.get(id=pk, state_id=2)
	service_collections= ServiceCollection.objects.filter(service_id=service.id)
	payment_methods= PaymentMethod.objects.all()
	card= Card.objects.filter(user_id=service.user_receiving.user.id)[:1]
	collections= Collection.objects.filter(state_id=1)
	publications_secondary=Publication.objects.filter(state=1)
	publications_secondary = [publications_secondary[x:x+2] for x in range(0, len(publications_secondary), 2)]
	context= {
	 "card": card,
	 "collections": collections,
	 "service_collections": service_collections,
	 "publications_secondary": publications_secondary,
	 "payment_methods": payment_methods,
	}
	cforms=[]
	if request.POST:
		updated_request = request.POST.copy()
		if request.POST.get('action') == 'update':
			if len(updated_request['prefix']) > 0:
				for x in updated_request['prefix'].split(","):
					qd = QueryDict(mutable=True)
					qd.update({"csrfmiddlewaretoken": updated_request.getlist('csrfmiddlewaretoken')[0], x+"-service": service.id, x+"-collection": updated_request.getlist(x+'-collection')[0], x+"-quantity":updated_request.getlist(x+'-quantity')[0]})
					cforms.append(ServiceCollectionForm(qd, prefix=x))
					del qd
			updated_request.update({"user_providing": request.user.id, "route": "service_front_associate_3"});
			form=ServiceForm(updated_request, instance= service)
			if form.is_valid() and all([cf.is_valid() for cf in cforms]):
				service_collections.delete()
				service_form=form.save(commit=False)
				service_form.promotion_category_percent= -service.user_receiving.category.discount
				service_form.promotion_category = -int(service.user_receiving.category.discount * service_form.price / 100)
				service_form.save()
				for cf in cforms:
					cf.save()
				return redirect('services:service_front_associate_4', pk=service.id)
			else:
				print(form.errors)			
				for cf in cforms:
					print(cf.errors)
		elif request.POST.get('action') == 'delete':
			updated_request.update({"user_providing": request.user.id, "state":4, "price":0, "route": "service_front_associate_3_delete"});
			form=ServiceForm(updated_request, instance= service)
			if form.is_valid():
				service_collections.delete()
				form.save()
				return redirect('services:service_front_associate')
			else:
				print(form.errors)
	else:
		form=ServiceForm(instance= service)
		cforms= [ServiceCollectionForm(prefix=str(x.collection.id), instance=x) for x in service_collections]
	context['cforms'] = cforms
	context['form'] = form
	return render (request,"services/service_front_associate_3.html",context)

def service_front_associate_4(request, pk):
	service= Service.objects.get(id=pk, state_id=2)
	service_collections= ServiceCollection.objects.filter(service_id=service.id).annotate(price= F('quantity') * F('collection__value'))
	total_collections= service_collections.aggregate(prices=Coalesce(Sum('price'), 0))
	context= {
		"service": service,
		"service_collections": service_collections,
		"initial_affectation": 0,
		"initial_affectation_percent": 0,
		"discount_increase_policies": 0,
		"discount_increase_policies_percent": 0
	}
	total= service.price
	hour_make_naive= timezone.make_naive(service.time_stop).time()
	rate= Rate.objects.filter(value=total)
	discount_increase_policies= total * rate[0].discount_increase / 100
	if service.initial_affectation_bool:
		time_zone= Time_Zone.objects.filter(hour_start__lte=hour_make_naive, hour_end__gte=hour_make_naive)
		initial_affectation= total * time_zone[0].value / 100
		context['initial_affectation'] = -int(initial_affectation)
		context['initial_affectation_percent'] = -time_zone[0].value
		total+=context['initial_affectation']

	if datetime.strptime('17::00::00', '%H::%M::%S').time() <= hour_make_naive < datetime.strptime('20::00::00', '%H::%M::%S').time():
		context['discount_increase_policies'] = int(discount_increase_policies)
		context['discount_increase_policies_percent'] = rate[0].discount_increase
		total+=context['discount_increase_policies']

	if datetime.strptime('11::00::00', '%H::%M::%S').time() <= hour_make_naive < datetime.strptime('13::00::00', '%H::%M::%S').time():
		context['discount_increase_policies'] = -int(discount_increase_policies)
		context['discount_increase_policies_percent'] = -rate[0].discount_increase
		total+=context['discount_increase_policies']
	total+=service.promotion_category
	total+=total_collections['prices']
	total= round(total/100)*100
	context["total"]=total
	if request.POST:
		service.initial_affectation = context['initial_affectation']
		service.initial_affectation_percent = context['initial_affectation_percent']
		service.discount_increase_policies = context['discount_increase_policies']
		service.discount_increase_policies_percent = context['discount_increase_policies_percent']
		service.total = context["total"]
		service.state_id = 3
		for x in service_collections:
			x.total_price =  x.quantity * x.collection.value
			x.save()
		service.save()
		return redirect('services:service_front_associate')
	return render (request,"services/service_front_associate_4.html", context)	

def service_front_affiliate(request):
	# authentication_vimeo()
	locations=Location.objects.filter(user=request.user)
	publications=Publication.objects.filter(state=1)
	publications_secondary=publications.filter(main_publication=False)
	publications_secondary = [publications_secondary[x:x+2] for x in range(0, len(publications_secondary), 2)]
	publication_main=publications.filter(main_publication=True)[:1]
	extended_user=Extended_User.objects.get(user_id= request.user.id)
	card= Card.objects.filter(user_id=request.user.id)[:1]
	context={
		"locations":locations,
		"publications_secondary": publications_secondary,
		"publication_main": publication_main,
		"extended_user":extended_user,
		"card":card
	}
	if request.POST:
		ramdom_code=get_random_string(length=6, allowed_chars='1234567890')
		updated_request = request.POST.copy()
		updated_request.update({'user_receiving': request.user.id, 'code':ramdom_code, 'state': 1, "route": "service_front_affiliate"})
		form=ServiceForm(updated_request)
		if form.is_valid():
			service=form.save()
			context['service']=service
			return render(request,"services/service_front_affiliate.html",context)
		else:
			print(form.errors)
			context['form'] = form
	return render(request,"services/service_front_affiliate.html",context)

def travel_history(request):
	services= Service.objects.filter(Q(user_receiving_id=request.user.id)|Q(user_providing_id=request.user.id)).order_by("-creation_date")
	extended_user=Extended_User.objects.get(user_id= request.user.id)
	card= Card.objects.filter(user_id=request.user.id)[:1]
	
	context={
		"services": services,
		"extended_user":extended_user,
		"card":card,
	}
	
	return render (request,"services/travel_history.html",context)

def travel_history_back(request, pk= None):
	collections= Collection.objects.filter(state_id=1)
	type_pqrs=TypePqr.objects.all()
	cities=City.objects.all()
	states=State_Pqr.objects.all()
	states_service= StateService.objects.all()
	subquery= Card.objects.filter(user_id=OuterRef('user_receiving')).values('code')
	subquery1= Card.objects.filter(user_id=OuterRef('user_providing')).values('code')
	services = Service.objects.all().prefetch_related(models.Prefetch('pqr_set', queryset=Pqr.objects.select_related('service'),  to_attr='pqr_records'), models.Prefetch('servicecollection_set', queryset=ServiceCollection.objects.select_related('service'),  to_attr='service_collection_records')).annotate(cod_receiving= Subquery(subquery[:1]), cod_providing= Subquery(subquery1[:1]) ).order_by("-creation_date")
	bar_search= request.GET.get('bar_search', "")
	city_search= request.GET.get('city_search', "")
	filter_state= request.GET.get("filter_state", "")
	
	context={
		'collections': collections,
		'type_pqrs': type_pqrs,
		'cities': cities,
		'states': states,
		'states_service': states_service,
		'active_travel_history':'text-dark',
		'name': 'Historial de viajes'
	}
	if pk:
		service= services.get(id=pk)
		context['service'] = service
		pqr= None
		if bool(service.pqr_records):
			pqr = service.pqr_records[0]
			context['pqr'] = pqr
		context['modal'] = 'show'

	if bar_search != "":
		services= services.filter(Q(user_receiving__document_number__icontains = bar_search)|Q(user_receiving__cell_phone__icontains = bar_search)|Q(user_receiving__phone_secondary__icontains = bar_search)|Q(user_providing__document_number__icontains = bar_search)|Q(user_providing__cell_phone__icontains = bar_search)|Q(user_providing__phone_secondary__icontains = bar_search)|Q(cod_receiving__icontains = bar_search)|Q(cod_providing__icontains = bar_search))
	if filter_state != "":
		services= services.filter(state_id=filter_state)
	if city_search != "":
		services= services.filter(location__city_id=city_search)

	context['services'] = services
	if request.POST:
		updated_request = request.POST.copy()
		if pqr:
			updated_request.update({'user_answer': request.user.id, 'modification_date': timezone.now(), "route": "service_edit"})
			form = PqrForm(updated_request, instance=pqr)
			if form.is_valid():
				form.save()
				return redirect('services:travel_history_back')
			else:
				print(form.errors)
				context['form'] = form
		else:
			updated_request.update({'service': service.id, 'user_answer': request.user.id, 'modification_date': timezone.now(), "route": "service"})
			form = PqrForm(updated_request)
			form_service = ServiceForm(updated_request, instance=service)
			if  form.is_valid() and form_service.is_valid():
				form.save()
				form_service.save()
				return redirect('services:travel_history_back')
			else:
				print(form.errors)
				print(form_service.errors)
				context['form'] = form
				context['form_service'] = form_service

	page = request.GET.get('page', 1)
	paginator = Paginator(services,20)
	try:
		services = paginator.page(page)
	except PageNotAnInteger:
		services = paginator.page(1)
	except EmptyPage:
		services = paginator.page(paginator.num_pages)
	context['services']= services

	return render (request,"services/travel_history_back.html",context)
