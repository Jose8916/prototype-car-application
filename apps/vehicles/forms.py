from django import forms
from django.db.models import Q
from apps.vehicles.models import *

class VehicleForm(forms.ModelForm):	

	invitation_code = forms.CharField(
		label="Código usuario",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
        }) 
	) 
   
	class Meta:
		model = Vehicle
		fields = ('technomechanical','soat','photo','plate','brand','line','model','technomechanical_date','soat_date','state','tarjeton','tarjeton_date')
		labels = {
            'technomechanical':('Tecnomecanica'),
            'soat':('Soat'),
            'photo':('Foto vehiculo'),
            'tarjeton':('Foto tarjeton'),
            'plate':('Placa'),
			'brand':('Marca'),
            'line':('Linea'),
            'model':('Modelo'),
            'technomechanical_date':('Tecnomecanica | fecha de vencimiento'),
			'soat_date':('SOAT | fecha de vencimiento'),
            'tarjeton_date':('Tarjeton | fecha vencimiento'),
			'state' : ('Estado'),
        }       
		widgets = {
            'technomechanical': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'soat': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'photo': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'tarjeton': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'plate': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'brand': forms.TextInput(
                attrs={
                    'class' :'form-control',
                    'rows':'3'
                }
            ),
            'line': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'technomechanical_date': forms.TextInput(
                attrs={
                    "type":"date",
                    'class' :'form-control',
                }
            ),
            'soat_date': forms.TextInput(
                attrs={
                    "type":"date",
                    'class' :'form-control',
                }
            ),
            'tarjeton_date': forms.TextInput(
                attrs={
                    "type":"date",
                    'class' :'form-control',
                }
            ),
            'state' :forms.Select(
				attrs={
					'class' :'form-control',
                }
            ),
        }
		error_messages = {
            "model": {
                "required" : ("Debe de indicar modelo del vehiculo"),
            },
        } 
	def __init__(self,  *args, **kwargs):             
		super(VehicleForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.fields.pop("invitation_code")
	def clean(self):
		cleaned_data = super(VehicleForm, self).clean()
		plate = cleaned_data.get("plate")		
		invitation_code = cleaned_data.get("invitation_code")
		user = None
		if invitation_code:
			if not Card.objects.filter(code=invitation_code).exists():
				self.add_error('invitation_code','El código indicado no existe')
			else:
				obj_card = Card.objects.filter(code=invitation_code).first()
				user = obj_card.user
		else:
			user = self.instance.user
		if user:
			if self.instance.pk:
				resultado = Vehicle.objects.filter(user=user,plate = plate).exclude(pk=self.instance.pk) or None
			else:
				resultado = Vehicle.objects.filter(user=user,plate = plate) or None
			if resultado:
				id = str(resultado.first().id)
				self.add_error('plate','La placa indicada ya existe con el ID numero '+plate)

				