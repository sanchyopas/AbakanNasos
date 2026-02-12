from django import forms
from home.models import HomeTemplate
from shop.models import Category,Product
from branch.models import Branch

class OrderForm(forms.Form):
  name = forms.CharField()
  phone = forms.CharField()
  product = forms.CharField()
  branch = forms.ModelChoiceField(queryset=Branch.objects.all())

class CallbackForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()
    branch = forms.ModelChoiceField(queryset=Branch.objects.all())

class contactUsForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    product = forms.CharField()
    branch = forms.ModelChoiceField(queryset=Branch.objects.all())

