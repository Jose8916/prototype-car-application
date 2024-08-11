from django.db import models
from django.contrib.auth.models import *
from apps.states.models import *
from apps.users.models import *
	
class Vehicle(models.Model):
	user = models.ForeignKey(Extended_User, on_delete = models.CASCADE,null=True)
	plate = models.CharField(max_length=6, null=True)
	brand = models.CharField(max_length=30, null=True)
	line = models.CharField(max_length=30, null=True)
	model = models.IntegerField()
	photo = models.ImageField(verbose_name='foto',upload_to='vehiculos/', null=True)
	tarjeton = models.ImageField(verbose_name='tarjeton',upload_to='tarjeton/', null=True)
	tarjeton_date =  models.DateField(null=True)
	technomechanical =  models.FileField(null=True, upload_to='technomechanical/',default="")
	technomechanical_date =  models.DateField(null=True)
	soat =  models.FileField(null=True, upload_to='soat/',default="")
	soat_date =  models.DateField(null=True)
	editing_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='editing_user')
	state = models.ForeignKey(State, on_delete = models.CASCADE, default=1)
	is_active = models.BooleanField(default=False)
	use_condition = models.CharField(max_length=100, default="Libre")
	create_user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True, related_name='Vehicle_create_user')
	create_date = models.DateTimeField(null=True, default=timezone.now)
	modification_user = models.ForeignKey(Extended_User, on_delete=models.CASCADE, null=True, related_name='Vehicle_modification_user')
	modification_date = models.DateTimeField(null=True, default=timezone.now)
	