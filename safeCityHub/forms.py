from django import forms
from .models import Emergencies

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class emergencyForm(forms.Form):
    class Meta:
        model = Emergencies
        fields = ['incident_type', 'urgency_level', 'date_time', 'contact_number', 'description', 'proof', 'anonymous', 'longitude', 'latitude']