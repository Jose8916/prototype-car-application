from django.db import models
from django.contrib.auth.models import *
from django.utils.crypto import get_random_string
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from apps.states.models import *
from apps.regions.models import *

# Create your models here.
class DocumentType(models.Model):
	name = models.CharField(max_length = 50, null=True)

class Gender(models.Model):
	name = models.CharField(max_length = 50, null=True)

class Blood_Types(models.Model):
	name = models.CharField(max_length = 50, null=True)

class Category(models.Model):
	name = models.CharField(max_length = 50, null=True)
	discount= models.FloatField(default=0)
	
class Extended_User(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_user', primary_key=True)
	document_type = models.ForeignKey(DocumentType,on_delete=models.CASCADE,null=True)
	document_number= models.CharField(max_length = 20, null=True)
	date_birth = models.DateField(null=True)
	photo = models.ImageField(verbose_name='photo',upload_to='users/', null=True)
	gender = models.ForeignKey(Gender, on_delete = models.CASCADE, null=True)
	blood_type = models.ForeignKey(Blood_Types, on_delete = models.CASCADE, null=True)
	category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
	cell_phone = models.CharField(max_length = 10, null=True, default="")
	phone_secondary = models.CharField(max_length = 10, null=True)
	city = models.ForeignKey(City, on_delete = models.CASCADE, null=True)
	address = models.CharField(max_length = 100, null=True, default="")
	description_address = models.TextField(null=True, default="")
	favorite_station = models.CharField(max_length = 50, null=True)
	favorite_music = models.CharField(max_length = 50, null=True)
	contact_person_name = models.CharField(max_length = 150, null=True)
	contact_person_phone = models.CharField(max_length = 10, null=True)
	inviting_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='inviting_user')
	authorizing_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='authorizing_user')
	state = models.ForeignKey(State, on_delete = models.CASCADE, default=2)
	call = models.BooleanField(default=False)
	inactive_until = models.DateTimeField(null=True)
	contact_text_check = models.BooleanField(default=False)
	contact_experience_check = models.BooleanField(default=False)
	exchange_data_check = models.BooleanField(default=False)
	def __str__(self):
		return '{}'.format(self.user.first_name+" "+ self.user.last_name)
	def get_code_invitation(self):
		obj_card = Card.objects.filter(user_id=self.pk).first() or None
		if obj_card:
			return obj_card.code
		return None	
	def get_group_name(self):
		list_groups = self.user.groups.all()
		if list_groups:
			return list_groups[0].name
		return None

class Code(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length = 6, unique = True)
	created = models.DateTimeField(auto_now_add=True)
	used = models.BooleanField(default=False)

class TypeSubscription(models.Model):
	name = models.CharField(max_length = 10)
	days = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(365)])
	def __str__(self):
		return self.name
 

class Subscription(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	type_subscription = models.ForeignKey(TypeSubscription, on_delete=models.CASCADE)
	description = models.TextField(default="")
	price = models.FloatField(default=0, null=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	bonus_direct = models.BigIntegerField(default=0)
	bonus_indirect = models.BigIntegerField(default=0)
	def __str__(self):
		return str(self.group)+" - "+str(self.price)

class Coupon(models.Model):
	code = models.CharField(max_length=50)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
	used = models.BooleanField(default=False)
	create_date = models.DateTimeField(blank=True,null=True, default=timezone.now)
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	cell_phone = models.CharField(max_length = 10, null=True, default="")
	email = models.EmailField(null=True, default="")
	city = models.ForeignKey(City, on_delete = models.CASCADE)
	expiration_date = models.DateTimeField(blank=True,null=True, default=timezone.now)
	def get_group_name(self):
		list_groups = self.subscription.groups.all()
		if list_groups:
			return list_groups[0].name
		return None
	def get_activation_date(self):
		obj_invoice =  Invoice.objects.filter(coupon=self).first() or None
		if obj_invoice:
				return obj_invoice.create_date
		return None
	def get_used(self):
		if 	self.used:
			return "Si"
		return "No"
	
class Invoice(models.Model):
    state = models.ForeignKey(InvoiceState, on_delete=models.CASCADE, null= True)
    create_date = models.DateTimeField(null=True, default=timezone.now)
    total_price = models.FloatField(default=0, null=True)
    payment_method = models.CharField(max_length=30, null=True)
    id_transaction = models.CharField(max_length=30, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null= True)
    payment_reference = models.CharField(null=True, max_length=50, unique= True)
    user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True)

class ValidationCard(models.Model):
	name = models.CharField(max_length = 10, unique=True, null=True, default="")

class Card(models.Model):
	user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True)
	code = models.CharField(max_length = 10, unique=True)
	activation_code = models.CharField(max_length = 10, null=True)
	validation_card = models.ForeignKey(ValidationCard, on_delete=models.CASCADE, null=True)
	def payment_method(self):
		obj_card_subscription = CardSubscription.objects.filter(card=self).first() or None
		if obj_card_subscription:
			return obj_card_subscription.invoice.payment_method
		return ""
	def fecha_vencimiento(self):
		obj_card_subscription = CardSubscription.objects.filter(card=self).first() or None
		if obj_card_subscription:
			return obj_card_subscription.fecha_vencimiento()
		return ""
	def fecha_pago(self):
		obj_card_subscription = CardSubscription.objects.filter(card=self).first() or None
		if obj_card_subscription:
			return obj_card_subscription.payday
		return ""

class CardSubscription(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
	subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
	card = models.ForeignKey(Card, on_delete=models.CASCADE)
	payday = models.DateField(default=timezone.now)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	def fecha_vencimiento(self):
		return self.payday + timedelta(days=self.subscription.type_subscription.days)
 
class AllyCategory(models.Model):
    name = models.CharField(max_length = 200)
    create_date = models.DateTimeField(null=True, default=timezone.now)
    create_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='AllyCategory_create_user')
    def __str__(self):
        return self.name
    
class Ally(models.Model):
	photo_local_1 = models.ImageField(verbose_name='photo_local_1',upload_to='ally/')
	photo_local_2 = models.ImageField(verbose_name='photo_local_2',upload_to='ally/',null=True,blank=True)
	photo_local_3 = models.ImageField(verbose_name='photo_local_3',upload_to='ally/',null=True,blank=True)
	name = models.CharField(max_length = 200)
	description = models.TextField(null=False)
	number_mercantil = models.CharField(max_length = 100)
	category = models.ForeignKey(AllyCategory,on_delete = models.CASCADE)
	cell_phone = models.CharField(max_length = 10, null=True, default="")
	city = models.ForeignKey(City, on_delete = models.CASCADE, null=True)
	address = models.CharField(max_length = 100, null=True, default="")
	user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True, related_name='Ally_user')
	inactive_until = models.DateTimeField(null=True,blank=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	description_state = models.TextField(null=False,blank=True)
	create_user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True, related_name='Ally_create_user')
	create_date = models.DateTimeField(null=True, default=timezone.now)
	modification_user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True, related_name='Ally_modification_user')
	modification_date = models.DateTimeField(null=True, default=timezone.now)
	def __str__(self):
		return self.name

# class PromotionsByCategory(models.Model):
# 	category = models.ForeignKey(Category, on_delete = models.CASCADE)
# 	date_start = models.DateTimeField(null=True)
# 	date_end = models.DateTimeField(null=True)
