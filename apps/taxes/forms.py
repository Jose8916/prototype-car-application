from django import forms
from apps.taxes.models import *

class MembershipForm(forms.ModelForm):
    class Meta:
        model=Membership
        fields=[
            'name',
            'description',
        ]

# class PqrForm(forms.ModelForm):
#     class Meta:
#         model=Pqr
#         fields=[
#             'name',
#             'description',
#         ]

class AgreementForm(forms.ModelForm):
    class Meta:
        model=Agreement
        fields=[
            'name',
            'description',
        ]


class CollectionForm(forms.ModelForm):
    class Meta:
        model=Collection
        fields=[
            'name',
            'value',
            'dynamic',
            'state',
        ]

class Time_ZoneForm(forms.ModelForm):
    class Meta:
        model=Time_Zone
        fields=[
            'name',
            'description',
            'value',
            'hour_start',
            'hour_end',
            'state',
        ]

class Time_ZoneForm2(forms.ModelForm):
    class Meta:
        model=Time_Zone
        fields=[
            'value',
            'benefit'
        ]