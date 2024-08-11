from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.users.models import *
from apps.states.models import *
from apps.taxes.models import *
from apps.vehicles.models import *
# Create your models here.

class Service(models.Model):
	creation_date = models.DateTimeField(default=timezone.now)
	user_receiving =  models.ForeignKey(Extended_User, on_delete = models.CASCADE, null=True, related_name="user_receiving")
	user_providing = models.ForeignKey(Extended_User, on_delete = models.CASCADE, null=True, related_name="user_providing")
	vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE, null=True)
	location= models.ForeignKey(Location, on_delete = models.CASCADE, null=True)
	time_start = models.DateTimeField(null=True)
	time_stop = models.DateTimeField(null=True)
	initial_affectation_bool =  models.BooleanField(default=False)
	initial_affectation = models.IntegerField(default=0)
	initial_affectation_percent = models.FloatField(default=0)
	discount_increase_policies = models.IntegerField(default=0)
	discount_increase_policies_percent = models.FloatField(default=0)
	price = models.IntegerField(null=True)
	total = models.IntegerField(null=True)
	promotion_category_percent = models.FloatField(default=0)
	promotion_category = models.IntegerField(default=0)
	code = models.CharField(max_length=6, null=True)
	state = models.ForeignKey(StateService, on_delete = models.CASCADE, null=True)
	score = models.IntegerField(null=True, validators=[MaxValueValidator(5), MinValueValidator(1)])
	flag_call =  models.CharField(max_length=2, null=True)
	payment_method = models.ForeignKey(PaymentMethod, on_delete = models.CASCADE, null=True)
	


class TypePqr(models.Model):
	name = models.CharField(max_length = 100, null=True)

class Pqr(models.Model):
	type_pqr = models.ForeignKey(TypePqr, on_delete = models.CASCADE, null=True)
	description = models.TextField(default="", null=True)
	creation_date = models.DateTimeField(auto_now_add=True)
	modification_date = models.DateTimeField(default=timezone.now, null=True)
	state = models.ForeignKey(State_Pqr, on_delete = models.CASCADE, default=1)
	service = models.ForeignKey(Service, on_delete = models.CASCADE, null=True)
	user_question = models.ForeignKey(Extended_User, on_delete = models.CASCADE, null=True, related_name="user_question")
	user_answer = models.ForeignKey(Extended_User, on_delete = models.CASCADE, null=True, related_name="user_answer")

class History_Pqr(models.Model):
	pqr = models.ForeignKey(Pqr, on_delete = models.CASCADE,null=True)
	modification_date = models.DateTimeField(auto_now_add=True)
	state = models.CharField(max_length = 500, null=True)
	user_answer = models.ForeignKey(User, on_delete=models.CASCADE)

class ServiceCollection(models.Model):
	service = models.ForeignKey(Service, on_delete = models.CASCADE)
	collection = models.ForeignKey(Collection, on_delete = models.CASCADE)
	quantity = models.IntegerField()
	total_price = models.IntegerField(null=True)


class Publication(models.Model):
    photo = models.ImageField(verbose_name='photo', upload_to='publications/')
    url = models.CharField(max_length=500, null=True)
    main_publication = models.BooleanField(default=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    # Agregue campos // ulises
    fecha_desde_vigencia = models.DateField(null=True,blank=True,verbose_name='Fecha Desde Vigencia')
    fecha_hasta_vigencia = models.DateField(null=True,blank=True,verbose_name='Fecha Hasta Vigencia')
    orden = models.PositiveIntegerField(verbose_name='Orden')
