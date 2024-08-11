from django import forms
from apps.guests.models import balance_wallet, wallet
from apps.users.models import Card

class FormBalance(forms.Form):
    codigo_invitacion = forms.CharField(
		label="Código usuario",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
            'placeholder' :'Codigo de usuario', 
        }) 
	)
    def clean(self):
        cleaned_data = super(FormBalance, self).clean()
        codigo_invitacion = cleaned_data.get("codigo_invitacion")
        if codigo_invitacion:
            if not Card.objects.filter(code=codigo_invitacion).exists():
                self.add_error('codigo_invitacion','El código indicado no existe')

class FormCreateRecharge(forms.ModelForm):
   
    invitation_code = forms.CharField(
		label="Código usuario",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
        }) 
	)
   
    class Meta:       
        model = balance_wallet
        fields = ('amount',)
        labels = {
            'amount':('Valor recarga'),
        }       
        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'min':0,
                    'max':10,
                    'autocomplete': 'off',
                    'class': 'form-control',                    
                }
            ),
        }
        error_messages = {
            "amount": {
                "required" : ("Debe de indicar un valor de recarga"),
            },
        } 

    def clean(self):
        cleaned_data = super(FormCreateRecharge, self).clean()
        amount = cleaned_data.get("amount")               
        invitation_code = cleaned_data.get("invitation_code")
        if amount < 1:
            self.add_error('amount','Debe de indicar un numero mayor a 0')
        if invitation_code:
            if not Card.objects.filter(code=invitation_code).exists():
                self.add_error('invitation_code','El código indicado no existe')
                
class FormCreateTransfer(forms.ModelForm):
   
    invitation_code_origin = forms.CharField(
		label="Código usuario origen",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
        }) 
	)
    invitation_code_destination = forms.CharField(
		label="Código usuario destino",  
        required=True, 
        widget=forms.TextInput(attrs={ 
            'class' :'form-control', 
        }) 
	)
   
    class Meta:       
        model = balance_wallet
        fields = ('amount',)
        labels = {
            'amount':('Valor recarga'),
        }       
        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'min':0,
                    'max':10,
                    'autocomplete': 'off',
                    'class': 'form-control',                    
                }
            ),
        }
        error_messages = {
            "amount": {
                "required" : ("Debe de indicar un valor de recarga"),
            },
        } 

    def clean(self):
        cleaned_data = super(FormCreateTransfer, self).clean()
        amount = cleaned_data.get("amount")               
        invitation_code_origin = cleaned_data.get("invitation_code_origin")
        invitation_code_destination = cleaned_data.get("invitation_code_invitation_code_destination")
        if amount < 1:
            self.add_error('amount','Debe de indicar un numero mayor a 0')
        if invitation_code_origin:
            if not Card.objects.filter(code=invitation_code_origin).exists():
                self.add_error('invitation_code_origin','El código indicado de origen no existe')
            else:
                obj_card = Card.objects.filter(code=invitation_code_origin).first()
                obj_extended_user = obj_card.user
        if invitation_code_destination:
            if not Card.objects.filter(code=invitation_code_destination).exists():
                self.add_error('invitation_code_destination','El código indicado de destino no existe')        
        wallet_origin = wallet.objects.filter(user=obj_extended_user.user).first() or None
        if wallet_origin:
            if wallet_origin.balance < amount:
                self.add_error('amount','La cantidad indicada supera el saldo del usuario')        
        else:
            self.add_error('invitation_code_origin','El código indicado no posee una wallet')        
        