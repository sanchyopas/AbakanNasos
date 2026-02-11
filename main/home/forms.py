from django import forms
from home.models import HomeTemplate
from shop.models import Category,Product

class OrderForm(forms.Form):
  name = forms.CharField()

  phone = forms.CharField()

  product = forms.CharField()


class CallbackForm(forms.Form):
    name = forms.CharField()

    phone = forms.CharField()

    message = forms.CharField()

class contactUsForm(forms.Form):
    name = forms.CharField()

    phone = forms.CharField()

    product = forms.CharField()

