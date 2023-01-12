from django import forms
from django.core.validators import MinValueValidator
import datetime
from django.utils.timezone import now
class RequesterForm(forms.Form):
    ASSET_TYP = (
        ('LAPTOP','LAPTOP'),
        ('TRAVEL_BAG','TRAVEL_BAG'),
        ('PACKAGE','PACKAGE')
    )
    SENSITIVE_TYPE = (
        ('HIGHLY_SENSITIVE','HIGHLY_SENSITIVE'),
        ('SENSITIVE','SENSITIVE'),
        ('NORMAL','NORMAL')
    )
    FROM = forms.CharField()
    TO = forms.CharField()
    DATE_TIME = forms.DateField(widget=forms.DateInput(attrs = {'type': 'date','min': now().strftime('%Y-%m-%d')}))
    ASSET_COUNT = forms.IntegerField()
    ASSET_TYPE= forms.ChoiceField(choices=ASSET_TYP)
    ASSET_SENSITIVITY= forms.ChoiceField(choices=SENSITIVE_TYPE)
    WHOME_TO_DELIVER = forms.CharField()

class RiderForm(forms.Form):

    travel_mediu = (
        ('BUS','BUS'),
        ('CAR','CAR'),
        ('TRAIN','TRAIN')
    )
    FROM = forms.CharField()
    TO = forms.CharField()
    DATE_TIME = forms.DateField(widget=forms.DateInput(attrs = {'type': 'date','min': now().strftime('%Y-%m-%d')}))
    TRAVEL_MEDIUM= forms.ChoiceField(choices=travel_mediu)
    ASSET_COUNT = forms.IntegerField()


