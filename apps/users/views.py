from apps.guests.models import balance_wallet, wallet
import collections
from apps.users.models import *
from apps.regions.models import *
from apps.users.forms import *
from apps.users.externalApis import *
from django.http import HttpResponse
# django tools
import datetime
import pytz
from apps.users.resources import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q, F, Subquery, OuterRef, ExpressionWrapper, DateField, DateTimeField, DurationField
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import get_template

def login_user(request):
	context={}
	if request.user.is_authenticated:
		user = request.user
		if user.groups.filter(id=6).exists():
			return redirect('users:registration_two')
		elif user.groups.filter(id=4).exists() or user.groups.filter(id=7).exists():
			return redirect('users:index')
		else:
			today = timezone.now()
			card_subscription = CardSubscription.objects.filter(card__user_id=request.user.id, invoice__state_id=2).annotate(date_expiry= ExpressionWrapper(F('payday') + ExpressionWrapper(F('subscription__type_subscription__days')* 24 * 60 * 60 * 1000000, output_field=DurationField()), output_field=DateTimeField()))
			card_subscription = card_subscription.filter(date_expiry__gte = today)
			if card_subscription.filter(state_id=1).exists() and (user.groups.filter(id=1).exists() or user.groups.filter(id=5).exists()):
				request.session['user_activate'] = 'active_user'
				return redirect('services:service_front_affiliate')
			elif card_subscription.filter(state_id=1).exists() and user.groups.filter(id=2).exists():
				request.session['user_activate'] = 'active_user'
				return redirect('services:service_front_associate')
			elif card_subscription.filter(state_id=2).exists():
				request.session['user_activate'] = 'activate_card'
				return redirect('users:activate_card', pk=card_subscription.filter(state_id=2)[0].id)
			else:
				request.session['user_activate'] = 'subscription'
				return redirect('users:subscription')	
	if request.GET.get('register') != None:
		context['message'] = "Registro exitoso, puedes ingresar a la plataforma con las credenciales creadas"
	if request.POST:
		form=AuthenticationForm(None, request.POST)
		username = request.POST['username']
		password = request.POST['password']
		if form.is_valid():
			user = authenticate(username=username, password=password)
			if user is not None:
				obj_extended_user = Extended_User.objects.filter(pk=user.pk).first() or None
				if obj_extended_user:
					date_now = datetime.datetime.now()
					if obj_extended_user.inactive_until:
						fecha = obj_extended_user.inactive_until
						utc = fecha.replace(tzinfo=pytz.UTC)
						fecha = utc.astimezone(timezone.get_current_timezone())
						utc = date_now.replace(tzinfo=pytz.UTC)
						date_now = utc.astimezone(timezone.get_current_timezone())
						if fecha >= date_now: 
							form.add_error(None, "Usuario inactivo hasta la fecha "+str(fecha.strftime("%Y-%m-%d %H:%M")))
							context['form']=form 
							return render(request, "users/login_front.html", context)
				login(request, user)
				if user.groups.filter(id=6).exists():
					return redirect('users:registration_two')
				elif user.groups.filter(id=4).exists() or user.groups.filter(id=7).exists():
					return redirect('users:index')
				else:
					today = timezone.now()
					card_subscription = CardSubscription.objects.filter(card__user_id=request.user.id, invoice__state_id=2).annotate(date_expiry= ExpressionWrapper(F('payday') + ExpressionWrapper(F('subscription__type_subscription__days')* 24 * 60 * 60 * 1000000, output_field=DurationField()), output_field=DateTimeField()))
					card_subscription = card_subscription.filter(date_expiry__gte = today)
					if card_subscription.filter(state_id=1).exists() and (user.groups.filter(id=1).exists() or user.groups.filter(id=5).exists()):
						request.session['user_activate'] = 'active_user'
						return redirect('services:service_front_affiliate')
					elif card_subscription.filter(state_id=1).exists() and user.groups.filter(id=2).exists():
						request.session['user_activate'] = 'active_user'
						return redirect('services:service_front_associate')
					elif card_subscription.filter(state_id=2).exists():
						request.session['user_activate'] = 'activate_card'
						return redirect('users:activate_card', pk=card_subscription.filter(state_id=2)[0].id)
					else:
						request.session['user_activate'] = 'subscription'
						return redirect('users:subscription')	
			else:
				form.add_error(None, "Usuario no encontrado")
		context['form']=form
	return render(request, "users/login_front.html", context)

def password_recovery(request):
	context={}
	if request.POST:
		form=PasswordResetForm(request.POST)
		if form.is_valid():
			# form.save()
			plaintext = get_template('users/email_recovery.txt')
			template_html= get_template('users/email_recovery.html')
			user= User.objects.filter(email=request.POST['email'].lower())[0]
			context = {
                'domain': "http://82.180.137.125:8021",
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
            }

			subject, from_email, to, cc = '¡ '+"Restaurar contraseña"+' !', 'ado@tarjetaxi.com', [user.email], ['pedro.balcazar@gmail.com']
			text_content = plaintext.render(context)
			html_content = template_html.render(context)
			msg = EmailMultiAlternatives(subject, text_content, from_email, to, cc=cc)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			messages.error(request, 'Se envio un correo siga las instrucciones para restaurar la contraseña.')
			return redirect('users:login')
		else:
			print(form.errors)
		context['form']=form
	return render(request, "users/password_recovery.html", context)	

def password_reset(request, uidb64, token):
	context={}
	uid = urlsafe_base64_decode(uidb64).decode()
	user = User.objects.get(pk=uid)
	if token == 'set_password':
		session_token = request.session.get('_password_reset_token')
		if default_token_generator.check_token(user, session_token) and request.POST:
			form=SetPasswordForm(user, request.POST)
			if form.is_valid():
				form.save()
				messages.error(request, 'El cambio de contraseña fue exitoso.')
				return redirect('users:login')
			else:
				print(form.errors)
			context['form']=form
	else:
		if default_token_generator.check_token(user, token):
			request.session['_password_reset_token'] = token
			redirect_url = request.path.replace(token, 'set_password')
			return HttpResponseRedirect(redirect_url)
	return render(request, "users/password_reset.html", context)

def logout_user(request):
    logout(request)
    return redirect('users:login')

# La vista de inicio.
def index(request):
	return render (request,"users/index.html")

def subscription(request):
	obj_extended_user = get_object_or_404(Extended_User,user=request.user)
	if obj_extended_user.photo is None or obj_extended_user.photo == "":
		messages.error(request, 'Debe de dirigirse primero a un punto de registro para complementear la información')
		return redirect('users:logout')
	subscription=Subscription.objects.filter(group_id= request.user.groups.all()[0].id)
	context={
		"subscription": subscription,
	}
	invoice= Invoice.objects.filter(user_id=request.user.id, state=1)
	if invoice.exists():
		invoice=invoice[0]
	else:
		invoice= Invoice(user_id=request.user.id, state_id=1)
		invoice.save()
	card_subscription= CardSubscription.objects.filter(invoice_id=invoice.id)
	card= Card.objects.filter(user_id=request.user.id)
	if request.POST:
		invoice.payment_reference=str(invoice.id)+"-"+get_random_string(length=6)
		invoice.save()
		request.POST = request.POST.copy()
		request.POST.update({'invoice': invoice.id, 'card': card[0].id, 'state': 2})
		form = CardSubscriptionForm(request.POST, instance=card_subscription[0]) if card_subscription.exists() else CardSubscriptionForm(request.POST)
	
		if form.is_valid():
			card_save=form.save()
			if request.POST.get('coupon', None):
				coupon= Coupon.objects.filter(code=request.POST['coupon'], used= False, subscription_id= card_save.subscription.id, state_id= 1).first() or None
				if coupon:
					date_today = timezone.now()					
					if coupon.expiration_date is None or coupon.expiration_date > date_today:						
						invoice.payment_method = "CUPON"
						invoice.coupon_id = coupon.id
						invoice.total_price = card_save.subscription.price 
						invoice.state_id =  2
						invoice.save()
						coupon.used = True
						coupon.save()
						return redirect('users:invoice', pk=invoice.id )
					else:
						form.add_error(None, "El codigó ya expiro, fecha de expiración "+coupon.expiration_date.strftime("%Y-%m-%d"))
				else:
					form.add_error(None, "Codigó no valido o no disponible para este plan.")
			else:
				context['card_save'] = card_save
		else:
			print(form.errors)
	else:
		form = CardSubscriptionForm(instance=card_subscription[0]) if card_subscription.exists() else None
	context['form'] = form
	return render (request,"users/subscription.html", context)

def subscription2(request, pk=None):
	subscriptions=Subscription.objects.all().order_by('group_id')
	type_subscriptions=TypeSubscription.objects.all()
	groups= Group.objects.all()
	states=State.objects.all()
	
	context={
     	"active_print_cards":'text-dark',
		'subscriptions': subscriptions,
		'type_subscriptions': type_subscriptions,
		'groups': groups,
		'states': states,
	}

	if pk:
		subscription = subscriptions.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk

	if request.POST:
		request.POST = request.POST.copy()
		request.POST.update({"route": "subscription_edit"})
		form = SubscriptionForm(request.POST, instance=subscription) if pk else SubscriptionForm(request.POST)
		if form.is_valid():
			# print(form)
			subscription= form.save(commit=False)
			subscription.save()
			return redirect('users:subscription2')
		else:
			print(form.errors)
			context['modal'] = 'show'
	else:
		form = SubscriptionForm(instance=subscription) if pk else None
	context['form'] = form
		
	return render (request,"users/subscription2.html",context)

def invoices(request):
	invoices= Invoice.objects.filter(user__user_id=request.user.id).order_by("-create_date")[0]
	return redirect('users:invoice', pk=invoices.id )

def invoice(request, pk):
	context={}
	invoice= Invoice.objects.get(id= pk)
	card_subscription= CardSubscription.objects.filter(invoice=invoice)[0]
	if invoice.state_id == 1 or invoice.state_id == 3:
		if request.GET.get('id'):
			response_verify = status_transaction(request.GET.get('id'))
		elif invoice.id_transaction:
			response_verify = status_transaction(invoice.id_transaction)
		else:
			#crea un objeto con status_code en None empujado para poder hacer la validacion
			response_verify = collections.namedtuple("ObjectName", {"status_code": None}.keys())(*{"status_code": None}.values())
		if  response_verify.status_code == 200:
			invoice.payment_method= response_verify.json()['data']['payment_method_type']
			invoice.id_transaction= response_verify.json()['data']['id']
			invoice.create_date= response_verify.json()['data']['created_at']
			invoice.total_price= response_verify.json()['data']['amount_in_cents']/100
			if response_verify.json()['data']['status'] == "APPROVED":
				invoice.state_id= 2
				request.session['user_activate']= "activate_card"
				asigna_comision(invoice)
			elif response_verify.json()['data']['status'] == "DECLINED":
				invoice.state_id= 4
			elif response_verify.json()['data']['status'] == "VOIDED":
				invoice.state_id= 5
			elif response_verify.json()['data']['status'] == "ERROR":
				invoice.state_id= 6
			elif response_verify.json()['data']['status'] == "PENDING":
				invoice.state_id= 3
			invoice.save()
	elif invoice.state_id == 2 and request.session['user_activate'] == "subscription":
			request.session['user_activate']= "activate_card"
	context["invoice"] = invoice
	context["card_subscription"] = card_subscription
	try:
		a=0
	except Exception as e:
		context['error'] = "No tiene facturas asignadas"
	return render(request, "users/invoice.html", context)

def asigna_comision(obj_invoice):
	if obj_invoice.coupon:
		return False
	obj_subscription = CardSubscription.objects.get(invoice=obj_invoice)
	amount = obj_subscription.subscription.bonus_direct
	obj_extended_user_origin = obj_invoice.user
	paymenth_method = obj_invoice.payment_method
	transaction_number = obj_invoice.id_transaction
	obj_wallet = wallet.objects.get(user=obj_extended_user_origin.inviting_user)
	# Comision afiliado directo
	balance_wallet.objects.create(
		type_movement_id = 4,
		amount = amount,
		wallet = obj_wallet,
  		payment_method = paymenth_method,
		name = "",
		transaction_number = transaction_number,
		user_bonus_origin = obj_extended_user_origin,
		type_bonus = "1",
		card_subscription = obj_subscription,
		create_date = timezone.now(),  
		create_user = obj_invoice.user.user,
	)
	obj_wallet.balance += amount
	obj_wallet.save()
	obj_extended_user_direct = Extended_User.objects.filter(user=obj_extended_user_origin.inviting_user).first() or None
	if obj_extended_user_direct:
		# Comision afiliado indirecto
		amount = obj_subscription.subscription.bonus_indirect
		obj_wallet = wallet.objects.get(user=obj_extended_user_direct.inviting_user)
		balance_wallet.objects.create(
			type_movement_id = 5,
			amount = amount,
			wallet = obj_wallet,
			payment_method = paymenth_method,
			name = "",
			transaction_number = transaction_number,
			user_bonus_origin = obj_extended_user_origin,
			type_bonus = "2",
			card_subscription = obj_subscription,
			create_date = timezone.now(),  
			create_user = obj_invoice.user.user,
		)
		obj_wallet.balance += amount
		obj_wallet.save()
	return True
    

def registration(request):
	genders= Gender.objects.all()
	blood_types=Blood_Types.objects.all()
	groups= Group.objects.filter(id__in=[1, 2, 3, 5])
	document_types= DocumentType.objects.all()
	categories= Category.objects.all() 
	cities= City.objects.filter(state=1, department__state=1, department__country__state=1)
	context={
     	'genders': genders,
		'blood_types': blood_types,
		"groups": groups,
		"document_types": document_types,
		"categories": categories,
		"cities": cities
	}
	if request.POST:
		request.POST = request.POST.copy()
		new_email=request.POST['email'].lower()
		request.POST.update({'email': new_email, 'username': new_email, 'state':2})
		form=UserForm(request.POST)
		form2=ExtendUserForm(request.POST)
		if form.is_valid() and form2.is_valid():
			group= groups.get(id=request.POST['group'])
			user= form.save(commit=False)
			user.set_password(form.data['new_password'])
			user.save()
			user.groups.add(group)
			user2= form2.save(commit=False)
			card= Card.objects.get(code__exact=request.POST['invitation_code'])
			user2.user_id= user.id
			user2.inviting_user_id= card.user.user.id
			user2.save()
			wallet.objects.create(
				user=user
			)
			card_response=created_card_code(group.id, user2)
			message = "Hola, el código para proseguir con el registro en un punto autorizado es "+ str(card_response.code)
			send_mail(
				'Codigó de verificación',
				message,
				'ado@tarjetaxi.com',
				[user.email]
			)
			messages.error(request, 'Se envio un correo siga las instrucciones para terminar el proceso de registro.')
			return redirect('users:login')
		else:
			print(form.errors)
			print(form2.errors)
		context['form']=form
		context['form2']=form2	
	return render(request, "users/registration.html", context)

def registration_two(request):
	genders= Gender.objects.all()
	blood_types=Blood_Types.objects.all()
	subquery=Card.objects.filter(user=OuterRef('user_id'))
	extended_users = Extended_User.objects.filter(authorizing_user__isnull= True).annotate(code_card=Subquery(subquery.values('code')[:1]))
	context={
		'genders': genders,
		'blood_types': blood_types,
		'active_registration_two':'text-dark',
	}
	if request.GET.get('document') != None and request.GET.get('code') != None:
		try:
			extended_user = extended_users.get(document_number= request.GET.get('document'), code_card=request.GET.get('code'))
			context['extended_user'] = extended_user
		except Exception as e:
			print(e)
			context['error'] = "El usuario ya se encuentra registrado o no existe, compruebe que los datos ingresados estan correctos"
	if request.POST:
		request.POST = request.POST.copy()
		request.POST.update({'authorizing_user': request.user.id})
		form=ExtendUserForm(request.POST, request.FILES, instance=extended_user)
		if form.is_valid():
			form.save()
			return render(request, "users/registration_two.html", {'success': "Se guardaron los datos correctamente, el pago se debe realizar desde la cuenta del cliente"})
		else:
			print(form.errors)
		context['form']=form
	return render(request, "users/registration_two.html", context)

def created_card_code(some_id, instance):
	city = instance.city.cod
	ramdom_code=get_random_string(length=4, allowed_chars='1234567890')
	activation_code=get_random_string(length=6)
	document_number = instance.document_number
	cod = city+document_number[0]+document_number[-2:]+ramdom_code
	if some_id == 1:
		cod = "U"+cod
	elif some_id == 2:
		cod = "C"+cod
	elif some_id == 3:
		cod = "A"+cod
	elif some_id == 5:
		cod = "P"+cod
	card = Card.objects.create(user = instance, code = cod, activation_code = activation_code)
	return card

def operational_users(request, pk=None):
	extended_users = Extended_User.objects.filter(user__groups__id__in=[4, 6, 7]).order_by('user_id')
	groups= Group.objects.filter(id__in=[4, 6, 7])
	states= State.objects.filter(id__in=[1,2])
	cities=City.objects.all()
	bar_search= request.GET.get('bar_search', "")
	filter_group= request.GET.get("filter_group", "")
	context={
		# 'users':users,
		'extended_users':extended_users,
		'groups': groups,
		'states': states,
		'active_operational_users':'text-dark',
		'cities': cities,
	}
	if pk:
		extended_user = extended_users.get(user_id=pk)
		context['modal'] = 'show'
		context['pk'] = pk

	if bar_search != "":
		extended_users= extended_users.filter(Q(user__first_name__icontains = bar_search)|Q(user__last_name__icontains = bar_search)|Q(cell_phone__icontains = bar_search))
	if filter_group != "":
		extended_users = extended_users.filter(user__groups__id=filter_group)

	if request.POST:
		request.POST = request.POST.copy()		
		new_email=request.POST['email'].lower()
		request.POST.update({'email': new_email, 'username': new_email, "route": "extend_operative_create"})
		form = UserForm(request.POST, instance=extended_user.user) if pk else UserForm(request.POST)
		form2 = ExtendOperativeForm(request.POST, instance=extended_user) if pk else ExtendOperativeForm(request.POST)
		if form.is_valid() and form2.is_valid():
			user= form.save(commit=False)
			extended_user=form2.save(commit=False)
			if  form.data['new_password'] != '' and form.data['repeat_password'] != '':
				user.set_password(form.data['new_password'])
			user.is_active= True if form.data['state']== "1" else False
			user.save()
			inactive_until = request.POST['inactive_until']
			if inactive_until == "":
				inactive_until = None
			extended_user.inactive_until = inactive_until
			if not pk:
				group= groups.get(id=request.POST['group'])
				user.groups.add(group)
				# extended_user=form2.save(commit=False)
				extended_user.user_id=user.id
			extended_user.save()
			return redirect('users:operational_users')
		else:
			print(form.errors)
			print(form2.errors)
			context['modal'] = 'show'
	else:
		form = UserForm(instance=extended_user.user, initial = {'group': extended_user.user.groups.get(id=extended_user.user.groups.all()[:1]).id, 'state': 1 if extended_user.user.is_active else 2}) if pk else None
		form2 = ExtendOperativeForm(instance=extended_user) if pk else None
	context['form'] = form
	context['form2'] = form2
	# print(form2)

	page = request.GET.get('page', 1)
	paginator = Paginator(extended_users,20)
	try:
		extended_users = paginator.page(page)
	except PageNotAnInteger:
		extended_users = paginator.page(1)
	except EmptyPage:
		extended_users = paginator.page(paginator.num_pages)
	context['extended_users']= extended_users

	return render(request, "users/operational_users.html", context)

def print_cards(request, pk=None):
	cards = Card.objects.all().order_by('user_id')
	validation_cards = ValidationCard.objects.all().order_by('id')
	groups= Group.objects.filter(id__in=[1, 2, 3, 5])
	cities=City.objects.all()
	states=State_Pqr.objects.all()
	categories = Category.objects.all()
	bar_search= request.GET.get('bar_search', "")
	filter_group= request.GET.get("filter_group", "")
	category_group= request.GET.get("category_group", "")
	context={
		'cards': cards,
		'active_print_cards': 'text-dark',
		'groups': groups,
  		'categories': categories,
		'cities': cities,
		'states': states,
		'validation_cards': validation_cards,
	}

	if pk:
		card = cards.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk

	if bar_search != "":
		cards= cards.filter(Q(user__document_number__icontains = bar_search)|Q(user__cell_phone__icontains = bar_search)|Q(user__phone_secondary__icontains = bar_search)|Q(code__icontains = bar_search))
	if filter_group != "":
		cards = cards.filter(user__user__groups__id=filter_group)
	if category_group != "":
		cards = cards.filter(user__category__id=category_group)
	
	if request.GET.get('action') == 'download':
		dataset = CardExport().export(cards)
		response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="cards.xls"'
		return response

	if request.POST:
		request.POST = request.POST.copy()
		request.POST.update({"route": "print_cards_edit"})
		form = UserForm2(request.POST, instance=card.user.user) if pk else UserForm2(request.POST)
		form2 = ExtendOperativeForm(request.POST, instance=card.user) if pk else ExtendOperativeForm(request.POST)
		form3 = CardForm(request.POST, instance=card) if pk else CardForm(request.POST,)
		if form.is_valid() and form2.is_valid() and form3.is_valid():
			# print(form)
			# print(form2)
			# print(form3)
			user= form.save(commit=False)
			extended_user=form2.save(commit=False)
			validation_cards=form3.save(commit=False)
			user.username = user.email
			user.save()
			extended_user.save()
			validation_cards.save()
			return redirect('users:print_cards')
		else:
			print(form.errors)
			print(form2.errors)
			print(form3.errors)
			context['modal'] = 'show'
	else:
		form = UserForm2(instance=card.user.user) if pk else None
		form2 = ExtendOperativeForm(instance=card.user) if pk else None
		form3 = CardForm(instance=card) if pk else None
	context['form'] = form
	context['form2'] = form2
	context['form3'] = form3
		
	
	page = request.GET.get('page', 1)
	paginator = Paginator(cards,20)
	try:
		cards = paginator.page(page)
	except PageNotAnInteger:
		cards = paginator.page(1)
	except EmptyPage:
		cards = paginator.page(paginator.num_pages)
	context['cards']= cards
	return render (request,"users/print_cards.html",context)

def profile_front(request):
	context={
	}
	return render (request,"users/profile_front.html",context)

def categories(request,pk=None):
	categories = Category.objects.all()
	context={
		'active_categories':'text-dark',
		'categories':categories,
	}
	if pk:
		category = categories.get(id=pk)
		context['modal'] = 'show'
		context['category'] = category
		if request.POST.get('action') == 'create':
			form=CategoryForm(request.POST, instance=category)
			if form.is_valid():
				form.save()
				return redirect('users:categories')
			else:
				context['form'] = form
				context['modal'] = 'show'
	else :
		if request.POST.get('action') == 'create':
			form = CategoryForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('users:categories')
			else:
				context['form'] = form
				context['modal'] = 'show'
	return render(request, "users/categories.html",context)

def coupons(request, pk=None):
	coupons = Coupon.objects.all().order_by("-id")
	states = State.objects.all().order_by("name")
	subscriptions = Subscription.objects.filter(state=1)
	cities = City.objects.filter(state=1)
	context={
		'active_coupons':'text-dark',
		'coupons': coupons,
		'subscriptions': subscriptions,
		'states':states,
		'cities':cities
	}
	if pk:
		coupon = coupons.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk
	if request.POST:
		# request.POST = request.POST.copy()
		# request.POST.update({'country': 1 })
		form =  CouponForm(request.POST, instance=coupon) if pk else CouponForm(request.POST)
		if form.is_valid():
			obj_coupon = form.save(commit=False)
			if obj_coupon.expiration_date:
				obj_coupon.expiration_date = obj_coupon.expiration_date.replace(hour=23,minute=59,second=59)
			obj_coupon.save()
			return redirect('users:coupons')
		else:
			context['modal'] = 'show'
	else:
		form = CouponForm(instance=coupon) if pk else None
	context['form'] = form
	return render (request,"users/coupons.html",context)

def registration_old(request,code=None):
	request.session.flush()
	# x = Invitation_Codes.objects.filter(Q(name=code)&Q(used=False))
	# if x.exists() and code:
	# 	code = code
	# else :
	# 	if request.path!=reverse('users:registration'):
	# 		return redirect('users:registration')
	cities=City.objects.all().order_by("name").exclude(
		Q(state=3)|
		Q(department__state__in=[2,3])|
		Q(department__country__state__in=[2,3])
	)
	documents = DocumentType.objects.all().order_by("name")
	groups = Group.objects.all().order_by("id")
	context = {
		'groups': groups,
		'cities' : cities,
		'documents' : documents,
		# 'code' : code
	}
	if request.method=='POST':
		updated_request = request.POST.copy()
		new_email=request.POST['email'].lower()
		updated_request.update({'email': new_email, 'username': new_email })
		# formAfiliate = AfiliateForm(updated_request)
		formExtendUser = ExtendUserForm(updated_request)
		formUser = UserForm(updated_request)
		if request.POST.get('new_code') != None:
			Code.objects.filter(email=new_email, used=False).delete()
		if formExtendUser.is_valid() and formUser.is_valid():
			group = groups.get(id=request.POST['group'])
			code_exists = Code.objects.filter(email=new_email, used=False)
			if not code_exists.exists():
				ramdom_code=get_random_string(length=6, allowed_chars='1234567890')
				send_mail('Bienvenido a la comunidad taxis amarillos', "Utiliza este código para completar tu registro en nuestra plataforma: "+ ramdom_code, "pedro@eurekadms.com", [new_email])
				code_create=Code(name=ramdom_code, email=new_email, used=False)
				code_create.save()
			code= request.POST.get('code', None)
			if code:
				code_exists = Code.objects.filter(name=code, email=new_email, used=False)
				if code_exists.exists():
					code_exists=code_exists.get(id=code_exists[0].id)
					code_exists.used=True
					code_exists.save()
					user = formUser.save(commit=False)
					user.set_password(formUser.data['new_password'])
					# user._group=group.name
					user.save()
					user.groups.add(group)
					extend = formExtendUser.save(commit=False)
					extend.user_id=user.id

					print("group", group.id)
					if group.id == 1:
						membership_type = Affiliate(user_id=user.id)
					elif group.id == 2:
						membership_type = Associate(user_id=user.id)
					elif group.id == 3:
						membership_type = Ally(user_id=user.id)
					extend.save()
					membership_type.save()
					created_card_code(group.id, extend)
					return redirect('/login/?register')
				else:
					formExtendUser.add_error(None, "Codigó no valido")
					context['code_verify'] = code
					context['code_error'] = "Codigó no valido"
					context['modal'] = 'show'
			else:
				formExtendUser.add_error(None, "No existe el codigó")
				context['modal'] = 'show'
		context['formUser'] = formUser
		context['formExtendUser'] = formExtendUser
	return render (request,"users/registration.html",context)

def users(request, pk=None):
	users = Extended_User.objects.all()
	context={
		'users':users,
		'active_users':'text-dark',
	}
	if pk:
		user= user.get(user_id=request.user.id)
		context['modal'] = 'show'
		context['user'] = user
	return render(request, "users/users.html", context)


def activate_cards(request):
	card_subscription = CardSubscription.objects.filter(card__user_id=request.user.id, invoice__state_id=2, state_id=2).annotate(date_expiry= ExpressionWrapper(F('payday') + ExpressionWrapper(F('subscription__type_subscription__days')* 24 * 60 * 60 * 1000000, output_field=DurationField()), output_field=DateTimeField()))
	pk = card_subscription[0].id if card_subscription.exists() else 0 
	return redirect('users:activate_card', pk=pk )
	
def activate_card(request, pk):
	try:
		card = Card.objects.filter(user__user_id= request.user.id)[0]
		context={
			"card": card
		}
		card_subscription= CardSubscription.objects.get(id=pk)
		if request.method=='POST':	
			request.POST = request.POST.copy()
			request.POST.update({'user': request.user.id, "pk":card_subscription.card.id})
			form = ActiveCardForm(request.POST)
			if form.is_valid():
				request.session['user_activate']= "active_user"
				card_subscription.state_id = 1
				card_subscription.save()
				if request.user.groups.filter(id=1).exists() or request.user.groups.filter(id=5).exists():
					return redirect('services:service_front_affiliate')
				else:
					return redirect('services:service_front_associate')
			else:
				print(form.errors)
				context['modal'] = 'show'
			context['form'] = form
	except Exception as e:
		context['error'] = "No hay tarjetas para activar"
	return render (request,"users/activate_card.html", context)


def allys(request, pk=None):
	allys = Ally.objects.all().order_by('id')
	categorias = AllyCategory.objects.all()
	bar_search= request.GET.get('bar_search', "")
	filter_group= request.GET.get("filter_group", "")
	context={
		'allys': allys,
		'categorias': categorias,
		'active_allys': 'text-dark',
	}
	if pk:
		ally = allys.get(id=pk)
		context['modal'] = 'show'
		context['pk'] = pk
	if bar_search != "":
		allys= Ally.objects.filter(Q(city__name__icontains = bar_search)|Q(cell_phone__icontains = bar_search)|Q(name__icontains = bar_search))
	if filter_group != "":
		allys = Ally.objects.filter(category=filter_group)
	if request.GET.get('action') == 'download':
		dataset = AllyExport().export(allys)
		response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="allys.xls"'
		return response
	if request.POST:
		request.POST = request.POST.copy()
		request.POST.update({"route": "allys_edit"})
		form = AllysForm(request.POST,request.FILES, instance=ally) if pk else AllysForm(request.POST,request.FILES)
		if form.is_valid():
			obj_ally= form.save(commit=False)
			invitation_code = form.cleaned_data.get("invitation_code")
			if invitation_code:
				obj_card = Card.objects.filter(code=invitation_code).first()
				obj_user = obj_card.user
				obj_ally.user = obj_user			
			obj_ally.save()
			return redirect('users:allys')
		else:
			context['modal'] = 'show'
	else:
		form = AllysForm(instance=ally) if pk else AllysForm()
	context['form'] = form
	page = request.GET.get('page', 1)
	paginator = Paginator(allys,20)
	try:
		allys = paginator.page(page)
	except PageNotAnInteger:
		allys = paginator.page(1)
	except EmptyPage:
		allys = paginator.page(paginator.num_pages)
	context['allys']= allys
	return render (request,"users/allys.html",context)

def allys_two(request):
	context={
		'active_registration_allys':'text-dark',
		"form":AllysFormTwo(),
	}
	obj_extended_user = None
	if request.GET.get('code') != None:
		try:
			obj_card = Card.objects.get(code=request.GET.get('code'))
			obj_extended_user = obj_card.user
			context['extended_user'] = obj_extended_user
		except Exception as e:
			context['error'] = "El codigo indicado no existe"
	if request.POST and obj_extended_user:
		request.POST = request.POST.copy()
		request.POST.update({'authorizing_user': request.user.id})
		form=AllysFormTwo(request.POST, request.FILES)
		if form.is_valid():
			obj_ally = form.save(commit=False)
			obj_ally.user = obj_extended_user
			obj_ally.state_id = 1
			obj_ally.save()
			messages.success(request,'El aliado se ha creado correctamente')
			return redirect('users:allys_two')
		context['form']=form
	return render(request, "users/allys_two.html", context)
