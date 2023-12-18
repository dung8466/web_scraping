from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator
from django.utils import timezone

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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.Select(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class RegularUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        
class ShopUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'shop_name', 'email', 'phone', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'current_price', 'img', 'url']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'current_price': forms.TextInput(attrs={'class': 'form-control'}),
            'img': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)

