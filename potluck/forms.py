from django import forms
from .models import PotluckEvent, DishSignup
from django.contrib.auth.models import User

class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    organizer = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
class PotluckEventForm(forms.ModelForm):
    class Meta:
        model = PotluckEvent
        fields = '__all__'

class DishSignupForm(forms.ModelForm):
    class Meta:
        model = DishSignup
        fields = '__all__'
