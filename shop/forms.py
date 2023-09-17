from django import forms
from .models import Order
class Order_Form(forms.ModelForm):
    class Meta:
         model=Order
         fields=['first_name','last_name','phone_number','email','address','postal_code','country','city']