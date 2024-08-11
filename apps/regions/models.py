from django.db import models
from django.contrib.auth.models import *
from apps.states.models import *

# Create your models here.
class Country(models.Model):
	name = models.CharField(max_length = 40, null=True, unique=True, error_messages={'unique':"Este pais ya se encuentra registrado"})
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	class Meta:
		ordering = ["name"]

class Department(models.Model):
	name = models.CharField(max_length = 30, null=True)
	country = models.ForeignKey(Country, on_delete = models.CASCADE, null=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE)
	class Meta:
		ordering = ["name"]

class City(models.Model):
	name = models.CharField(max_length = 30, null=True)
	department = models.ForeignKey(Department, on_delete = models.CASCADE, null=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE)	
	cod = models.CharField(max_length = 2, null=True, unique=True)
	class Meta:
		unique_together = (('name', 'department'))
		ordering = ["name"]
	def __str__(self):
		return self.name
     

class Location(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	city = models.ForeignKey(City, on_delete = models.CASCADE, null	= True)
	name = models.CharField(max_length = 30, null=True)
	address = models.CharField(max_length= 100 , null=True)
	state = models.ForeignKey(State, on_delete = models.CASCADE)