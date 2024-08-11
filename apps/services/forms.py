from django import forms
from apps.services.models import *
from django.forms import ModelForm, ImageField
from django.core.files.images import get_image_dimensions

class PqrForm(forms.ModelForm):
    class Meta:
        model=Pqr
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(PqrForm, self).__init__(*args, **kwargs)
        if len(args)>0:
            context=args[0].dict()
            if context.get("route") == "pqr_edit":
                del self.fields['service']
                del self.fields['type_pqr']
                del self.fields['user_question']

            elif context.get("route") == "service_edit":
                del self.fields['service']
                del self.fields['type_pqr']
                del self.fields['user_question']

            elif context.get("route") == "pqr_front_create":
                del self.fields['service']
                del self.fields['user_answer']

class PqrForm2(forms.ModelForm):
    class Meta:
        model = Pqr
        fields = '__all__'

    def __init__(self, *args, **kwargs):
       super(PqrForm2, self).__init__(*args, **kwargs)
       self.fields['service'].required=False
       self.fields['user_question'].required=False
       self.fields['user_answer'].required=False

class PqrFormOperator(forms.ModelForm):
    class Meta:
        model=Pqr
        fields=['state', 'modification_date']

class ServiceForm(forms.ModelForm):
    code_verify = forms.CharField(required=False)
    action = forms.CharField(required=False)
    route = forms.CharField(required=False)
    image = ImageField(required=False)
    class Meta:
        model=Service
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(ServiceForm, self).__init__(*args, **kwargs) 
        if len(args)>0:
            context=args[0].dict()
            del self.fields['creation_date']
            del self.fields['promotion_category']
            del self.fields['promotion_category_percent']
            del self.fields['initial_affectation']
            del self.fields['initial_affectation_percent']
            del self.fields['discount_increase_policies']
            del self.fields['discount_increase_policies_percent']
            del self.fields['total']
            del self.fields['vehicle']
            if context.get("route") == "service_front_associate_3":
                del self.fields['user_receiving']
                del self.fields['location']
                del self.fields['code']
                del self.fields['state']
                del self.fields['time_start']
                del self.fields['time_stop']
                del self.fields['flag_call']
                del self.fields['score']
            if context.get("route") == "service_front_associate_3_delete":
                del self.fields['user_receiving']
                del self.fields['location']
                del self.fields['code']
                del self.fields['time_start']
                del self.fields['time_stop']
                del self.fields['flag_call']
                del self.fields['score']
                del self.fields['payment_method']
            elif context.get("route") == "service_front_affiliate":
                del self.fields['user_providing'] 
                del self.fields['time_start'] 
                del self.fields['time_stop']
                del self.fields['price']
                del self.fields['flag_call']
                del self.fields['score']
                del self.fields['payment_method']
            elif context.get("route") == "service":
                del self.fields['user_receiving']
                del self.fields['user_providing']
                del self.fields['price']
                del self.fields['location']
                del self.fields['code']
                del self.fields['state']
                del self.fields['time_start']
                del self.fields['time_stop']
                del self.fields['payment_method']

    def clean(self):
        cleaned_data = super().clean()
        price = self.cleaned_data.get("price")
        action = self.cleaned_data.get("action")
        if price and not (action == "delete" and price == 0):
            validation_rate=Rate.objects.filter(value=price)
            if not validation_rate.exists():
                self.add_error('price', 'Valor no valido, ingrese otro valor')

class ServiceCollectionForm(forms.ModelForm):
    class Meta:
        model=ServiceCollection
        fields='__all__'
    def __init__(self, *args, **kwargs): 
        super(ServiceCollectionForm, self).__init__(*args, **kwargs)
        del self.fields['total_price']

class PublicationForm(forms.ModelForm):
    class Meta:
        model=Publication
        fields='__all__'

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            w, h = get_image_dimensions(photo)
            if w != 500 or h != 500:
                raise forms.ValidationError ("Subir una imagen de 500*500 pixeles")
        return photo