from django.db import models
from django.contrib.auth.models import *

# Create your models here.
class State(models.Model):
	name = models.CharField(max_length = 50, null=True)
	def __str__(self):
		return self.name

class State_Pqr(models.Model):
	name = models.CharField(max_length = 50, null=True)
	def __str__(self):
		return self.name

class StateService(models.Model):
	name = models.CharField(max_length = 50, null=True)
	def __str__(self):
		return self.name

class InvoiceState(models.Model):
	name = models.CharField(max_length = 50, null=True)
	def __str__(self):
		return self.name