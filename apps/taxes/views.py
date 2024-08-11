from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.utils import timezone

from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from tablib import Dataset
import random

from apps.taxes.models import *
from apps.taxes.forms import *
from apps.taxes.resources import *
from apps.states.models import *
# Create your views here.
def membership(request):
	memberships = Membership.objects.all().order_by("name")
	context={
		'list' : memberships,
		'active_membership':'text-dark',
	}
	if request.POST:
		form=MembershipForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('taxes:membership')
		else:
			context['form'] = form
	return render (request,"taxes/collections.html",context)


def agreement(request):

	agreements = Agreement.objects.all().order_by("name")
	context={
		'list' : agreements,
		'active_agreement':'text-dark',
	}
	if request.POST:
		form=AgreementForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('taxes:agreement')
		else:
			context['form'] = form
	return render (request,"taxes/list.html",context)

def collections(request, pk=None):
	collections = Collection.objects.all().order_by("id")
	states = State.objects.all().order_by("name")
	context={
		'collections' : collections,
		'active_collections':'text-dark',
		'states' : states,
	}
	if pk:
		collection = collections.get(id=pk)
		context['modal'] = 'show'
		context['collection'] = collection
		if request.POST:
			form=CollectionForm(request.POST, instance=collection)
			if form.is_valid():
				form.save()
				return redirect('taxes:collections')
			else:
				context['form'] = form
	else:
		if request.POST:
			form=CollectionForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('taxes:collections')
			else:
				context['form'] = form
	return render (request,"taxes/collections.html",context)

def time_zone(request, pk=None):
	lists = Time_Zone.objects.all().order_by("id")
	states = State.objects.all().order_by("name")
	context={
		'lists' : lists,
		'active_time_zone':'text-dark',
		'states' : states,
	}
	if pk:
		time = Time_Zone.objects.get(id=pk)
		context['modal'] = 'show'
		context['time'] = time
		if request.POST.get('action') == 'create':
			form=Time_ZoneForm2(request.POST, instance=time)
			if form.is_valid():
				form.save()
				return redirect('taxes:time_zone')
			else:
				context['form'] = form
				context['modal'] = 'show'
	else:
		if request.POST:
			form=Time_ZoneForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('taxes:time_zone')
			else:
				context['form'] = form
	return render (request,"taxes/time_zone.html",context)

def rate(request, pk=None):
	lists = Rate.objects.all().order_by("id")
	context={
		'lists' : lists,
		'active_rate':'text-dark',
	}
	if request.GET.get('action') == 'export':
		rate_resource = RateExportResource()
		dataset = rate_resource.export(lists)
		response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="tarifas.xls"'
		return response
	elif request.POST.get('action') == 'import':
		servicio = RateExportResource()
		dataset = Dataset()
		news = request.FILES['myfile']
		imported_data = dataset.load(news.read(),format='xls')
		result = servicio.import_data(dataset, dry_run=True, raise_errors=False, collect_failed_rows = False)
		context["result"] = result
		if not result.has_errors():
			servicio.import_data(dataset, dry_run=False)
	return render (request,"taxes/rate.html", context)

# def job_benefits_policy():
# 	try:
# 		array_time= [{"hour_start": "11:00:00","hour_end": "11:59:59"}, {"hour_start": "13:00:00","hour_end": "13:59:59"}, {"hour_start": "22:00:00","hour_end": "23:59:59"} ]
# 		random_result= random.sample(array_time, 1)[0] 
# 		print(random_result["hour_start"])
# 		benefits_policy = BenefitsPolicy.objects.create(date=timezone.make_naive(timezone.now()).date(), hour_start= random_result["hour_start"], hour_end= random_result["hour_end"])
# 	except Exception as e:
# 		print(e)

# def initial_benefits_policy():
# 	scheduler = BackgroundScheduler()
# 	scheduler.start()
# 	trigger = CronTrigger(year="*", month="*", day="*", hour="18", minute="49", second="0")
# 	scheduler.add_job(job_benefits_policy, trigger=trigger, name="daily benefits_policy")
# 	while True:
# 		sleep(5)