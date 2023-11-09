from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProductNameForm(ModelForm):
    class Meta:
        model = ProductName
        fields = ('name',)

class CompareForm(ModelForm):
    class Meta:
        model = CompareName
        fields = ('name',)

price_choices = (
    ("", "All"),
    ("A", "Giá thấp > cao"),
    ("B", "Giá cao > thấp")
)


class FilterForm(forms.ModelForm):
    # Becasue this is a ModelForm, you don't need to redefine the fields of the form to use in a template
    class Meta:
        model = ProductFilter
        fields = "__all__" # Use all fields from the model. It is equal to ['place', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
