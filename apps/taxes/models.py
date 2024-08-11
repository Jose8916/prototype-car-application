from django.db import models
from apps.states.models import *
from apps.users.models import *
# Create your models here.
class Membership(models.Model):
	name = models.CharField(max_length = 50, null=True)
	description = models.TextField(null=True)

# class Pqr(models.Model):
# 	name = models.CharField(max_length = 50, null=True)
# 	description = models.TextField(null=True)

class Agreement(models.Model):
	name = models.CharField(max_length = 50, null=True)
	description = models.TextField(null=True)


class Collection(models.Model):
	name = models.CharField(max_length = 100, null=True)
	value = models.IntegerField()
	dynamic = models.BooleanField(default=False)
	state = models.ForeignKey(State, on_delete = models.CASCADE,default=1)
	image = models.ImageField(upload_to = 'collections', default='default_image.jpg')

class Time_Zone(models.Model):
	name = models.CharField(max_length = 50, null=True)
	description = models.TextField(null=True)
	value = models.FloatField()
	benefit = models.FloatField(default=0)
	hour_start = models.TimeField(null=True)
	hour_end = models.TimeField(null=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE,default=1)

class Rate(models.Model):
	unit = models.IntegerField(null = True)  
	value = models.IntegerField()
	discount_increase= models.FloatField()

# class BenefitsPolicy(models.Model):
# 	date = models.DateField(unique=True)  
# 	hour_start = models.TimeField()
# 	hour_end = models.TimeField()

class PaymentMethod(models.Model):
	name = models.CharField(max_length = 50, null=True)

		