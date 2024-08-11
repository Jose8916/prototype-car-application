from django import forms
from apps.regions.models import *

class CountryForm(forms.ModelForm):
    class Meta:
        model=Country
        fields=[
            'name',
            'state',
        ]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields=[
            'name',
            'country',
            'state',
        ]

class CityForm(forms.ModelForm):
    class Meta:
        model=City
        fields=[
            'name',
            'department',
            'cod',
            'state',
        ]
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(CityForm, self).__init__(*args, **kwargs)
        if instance:
            del self.fields['cod']

class LocationForm(forms.ModelForm):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length = 30, null=True)
    # address = models.CharField(max_length= 100 , null=True)
    # state = models.ForeignKey(State, on_delete = models.CASCADE
    class Meta:
        model=Location
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(LocationForm, self).__init__(*args, **kwargs)
        if instance:
            del self.fields['address']
            del self.fields['city']
            
        if len(args)>0:
            context=args[0].dict()
            if context['delete'] != None:
                del self.fields['name']



