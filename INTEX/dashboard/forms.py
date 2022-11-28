from django import forms
from .models import person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class PersonForm(forms.ModelForm):
    class Meta:
        model = person
        fields = '__all__'