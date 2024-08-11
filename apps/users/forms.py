from django import forms
from django.db.models import Q
from apps.users.models import *
from apps.states.models import *
from allauth.account.adapter import get_adapter
from django.contrib.auth import authenticate
from django.core.files.images import get_image_dimensions


class UserForm(forms.ModelForm):
	new_password=forms.CharField(widget=forms.PasswordInput())
	repeat_password=forms.CharField(widget=forms.PasswordInput())
	group=forms.ModelChoiceField(queryset=Group.objects.all())
	state=forms.ModelChoiceField(queryset=State.objects.filter(id__in=[1,2]))
	class Meta:
		model = User
		fields = [
		'first_name',
		'last_name',
		'email',
		'repeat_password',
		'new_password',
		'username', 
		'group',
		'state'
		]
	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required=True
		self.fields['last_name'].required=True
		self.fields['email'].required=True
		self.fields['new_password'].required=True
		self.fields['repeat_password'].required=True
		self.fields['group'].required=True
		self.fields['state'].required=True
		if instance:
			self.fields['new_password'].required=False
			self.fields['repeat_password'].required=False
			self.fields['group'].required=False

	#al ser una validacion de campo doble deberia estar en un clean general, algo a mejorar
	def clean_email(self):
		email = self.cleaned_data['email']
		validation=User.objects.filter(Q(email=email)|Q(username=email)).exclude(pk=self.instance.pk).exists()
		if validation:
			raise forms.ValidationError(('Email existente, favor ingrese un dato valido.'), code='invalid')
		return email

	def clean_new_password(self):
		new_password=self.cleaned_data.get('new_password')
		repeat_password=self.cleaned_data.get('repeat_password')
		if self.instance :
			if new_password!= '' or  repeat_password!= '':
				if new_password!=repeat_password :
					raise forms.ValidationError(('Las contraseñas deben ser iguales'), code='invalid')
				else:
					validation=get_adapter().clean_password(new_password)	
		else:
			if new_password!=repeat_password:
				raise forms.ValidationError(('Las contraseñas deben ser iguales'), code='invalid')
			else:
				validation=get_adapter().clean_password(new_password)
		return new_password

class ExtendUserForm(forms.ModelForm):
	#se agrega este valor para poder devolverlo en el form de errores, este campo no existe en el modelo, se podria agregra un clena_group para validar que el grupo enviado sea valido
	#se coloca empty para que retorne None cuando no se nevia el campo
	invitation_code=forms.CharField(empty_value=None)
	#user no se debe dejar al ser una llave forane uno a uno en los fields genera conflicto
	class Meta:
		model = Extended_User
		fields ='__all__'

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)
		super(ExtendUserForm, self).__init__(*args, **kwargs)
		del self.fields['user']
		if instance:
			#campos excluidos
			del self.fields['document_type']
			del self.fields['document_number']
			del self.fields['cell_phone']
			del self.fields['category']
			del self.fields['city']
			del self.fields['state']
			del self.fields['invitation_code']
			del self.fields['inviting_user']
			del self.fields['inactive_until']   			

			#campos no requeridos u opcionales
			self.fields['contact_person_name'].required= False
			self.fields['contact_person_phone'].required= False
			self.fields['favorite_station'].required= False
			self.fields['favorite_music'].required= False
			self.fields['phone_secondary'].required= False			
			self.fields['blood_type'].required= False			
			self.fields['gender'].required= False			
			self.fields['photo'].required= True
		else:
			del self.fields['date_birth']
			# del self.fields['gender']
			del self.fields['phone_secondary']
			# del self.fields['blood_type']
			del self.fields['favorite_station']
			del self.fields['favorite_music']
			del self.fields['address']
			del self.fields['description_address']
			del self.fields['photo']
			del self.fields['contact_person_name']
			del self.fields['contact_person_phone']
			del self.fields['inviting_user']
			del self.fields['authorizing_user']
			del self.fields['inactive_until']   			

	def clean_invitation_code(self):
		invitation_code = self.cleaned_data.get('invitation_code')
		if invitation_code:
			validation=Card.objects.filter(code=invitation_code).exists()
			if not validation:
				raise forms.ValidationError(('El código de invitación es invalido'), code='invalid')
		return invitation_code

	def clean_photo(self):
		photo = self.cleaned_data.get('photo')
		if photo:
			w, h = get_image_dimensions(photo)
			if w > 1200 or h > 1200:
				raise forms.ValidationError ("Subir una imagen que tenga maximo 1200 pixeles de alto y de ancho.")
		return photo 

class ExtendOperativeForm(forms.ModelForm):
    class Meta:
        model=Extended_User
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(ExtendOperativeForm, self).__init__(*args, **kwargs)
        if len(args)>0:
            context=args[0].dict()
            self.fields['inactive_until'].required= False
            if context.get("route") == "extend_operative_create":
                del self.fields['user']
                del self.fields['document_type']
                del self.fields['document_number']
                del self.fields['date_birth']
                del self.fields['photo']
                del self.fields['gender']
                del self.fields['blood_type']
                del self.fields['category']
                del self.fields['phone_secondary']
                del self.fields['favorite_station']
                del self.fields['favorite_music']
                del self.fields['contact_person_name']
                del self.fields['contact_person_phone']
                del self.fields['inviting_user']
                del self.fields['authorizing_user']
                del self.fields['state']
                del self.fields['call']
            elif context.get("route") == "print_cards_edit":
                del self.fields['user']
                del self.fields['document_type']
                del self.fields['document_number']
                del self.fields['date_birth']
                del self.fields['photo']
                del self.fields['gender']
                del self.fields['blood_type']
                del self.fields['category']
                del self.fields['city']
                del self.fields['favorite_station']
                del self.fields['favorite_music']
                del self.fields['contact_person_name']
                del self.fields['contact_person_phone']
                del self.fields['inviting_user']
                del self.fields['authorizing_user']
                del self.fields['state']
                del self.fields['call']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=[
            'name',
            'discount'
        ]

class CouponForm(forms.ModelForm):
    class Meta:
        model=Coupon
        fields='__all__'
        exclude = ('created_date',)
        

class CardSubscriptionForm(forms.ModelForm):
	class Meta:
		model=CardSubscription
		fields='__all__'
	def __init__(self, *args, **kwargs):
		super(CardSubscriptionForm, self).__init__(*args, **kwargs)
		self.fields['payday'].required=False

class ExtendUserStepTwoForm(forms.ModelForm):
	class Meta:
		model = Extended_User
		fields = '__all__'

class CardForm(forms.ModelForm):
    class Meta:
        model=Card
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(CardForm, self).__init__(*args, **kwargs)
        if len(args)>0:
            context=args[0].dict()
            if context.get("route") == "print_cards_edit":             
                del self.fields['user']
                del self.fields['code']
                del self.fields['activation_code']
				
class UserForm2(forms.ModelForm):
	password = forms.CharField(required=False, widget=forms.PasswordInput())
	first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'date_joined'] 
	def __init__(self, *args, **kwargs):
		super(UserForm2, self).__init__(*args, **kwargs)		
		if len(args)>0: 
			context=args[0].dict()
			if context.get("route") == "print_cards_edit":
				del self.fields['username']
				del self.fields['date_joined']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model=Subscription
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        if len(args)>0:
            context=args[0].dict()
            if context.get("route") == "subscription_edit":            
                del self.fields['group']
                del self.fields['type_subscription']


class PasswordResetForm(forms.Form):
	email = forms.EmailField(max_length=254)
	def clean_email(self):
		email = self.cleaned_data['email']
		validation=User.objects.filter(Q(email=email)).exists()
		if not validation:
			raise forms.ValidationError(('Este correo electronico no  esta asociado a ninguna cuenta.'), code='invalid')
		return email

class ActiveCardForm(forms.Form):
	user = forms.IntegerField()
	activation_code = forms.CharField(max_length=10)
	pk = forms.IntegerField()
	field_order = ['user', 'activation_code', 'pk']

	def clean(self):
		cleaned_data = super().clean()
		activation_code = self.cleaned_data.get("activation_code")
		user = self.cleaned_data.get("user")
		pk = self.cleaned_data.get("pk")
		print(self.cleaned_data)
		validation=Card.objects.filter(id=pk, activation_code=activation_code, user__user_id=user)
		print(validation)
		if not validation.exists():
			self.add_error('activation_code', 'El código de activación incorrecto.')

class AllysForm(forms.ModelForm):
	invitation_code = forms.CharField(
		label="Código usuario",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
        }) 
	) 
   
	class Meta:
		model = Ally
		fields = ('photo_local_1','photo_local_2','photo_local_3','name','description','number_mercantil','category','cell_phone','city','address','inactive_until','state','description_state')
		labels = {
            'photo_local_1':('Foto establecimiento 1'),
            'photo_local_2':('Foto establecimiento 2'),
            'photo_local_3':('Foto establecimiento 3'),
            'name':('Nombre'),
			'description':('Descripción establecimiento'),
            'number_mercantil':('Numero mercantil'),
            'category':('Categoria'),
            'cell_phone':('Teléfono'),
			'city':('Ciudad'),
			'address':('Dirección'),			
			'inactive_until':('Inactivo hasta'),
			'state':('Estado'),
   			'description_state':('Descripción estado'),
        }       
		widgets = {
            'photo_local_1': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'photo_local_2': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'photo_local_3': forms.FileInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class' :'form-control',
                    'rows':'3'
                }
            ),
            'number_mercantil': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class' :'form-control',
                }
            ),
            'cell_phone': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'city': forms.Select(
                attrs={
                    'class' :'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class' :'form-control',
                }
            ),
            'inactive_until': forms.TextInput(
                attrs={
                    "type":"datetime-local",
                    'class' :'form-control',
                }
            ),
            'state': forms.Select(
                attrs={
                    'class' :'form-control',
                }
            ),
            'description_state': forms.Textarea(
                attrs={
                    'class' :'form-control',
                    'rows':'3'
                }
            ),
        }
		error_messages = {
            "empelado": {
                "required" : ("Debe de indicar un empleado"),
            },
            "rol": {
                "required" : ("Debe de indicar un rol"),
            },
            "bodega": {
                "required" : ("Debe de indicar una bodega"),
            },
            "estado": {
                "required" : ("Debe de indicar un estado"),
            },
        } 
	def __init__(self,  *args, **kwargs):             
		super(AllysForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.fields.pop("invitation_code")
	def clean(self):
		cleaned_data = super(AllysForm, self).clean()
		name = cleaned_data.get("name")		
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
				resultado = Ally.objects.filter(user=user,name = name).exclude(pk=self.instance.pk) or None
			else:
				resultado = Ally.objects.filter(user=user,name = name) or None
			if resultado:
				id = str(resultado.first().id)
				self.add_error('name','El nombre indicado ya existe con el ID numero '+id)

class AllysFormTwo(AllysForm):
	def __init__(self,  *args, **kwargs):             
		super(AllysForm, self).__init__(*args, **kwargs)
		self.fields.pop("invitation_code")
		self.fields.pop("inactive_until")
		self.fields.pop("state")
		self.fields.pop("description_state")
		