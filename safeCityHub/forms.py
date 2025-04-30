from django import forms
from .models import Emergencies
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class emergencyForm(forms.Form):
    class Meta:
        model = Emergencies
        fields = ['incident_type', 'urgency_level', 'date_time', 'contact_number', 'description', 'proof', 'anonymous', 'longitude', 'latitude']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
