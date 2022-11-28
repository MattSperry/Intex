from django import forms
from .models import MovieData
 
class MovieDataForm(forms.ModelForm):
    class Meta:
        model = MovieData
        fields = '__all__'