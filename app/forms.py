from django import forms
from django.contrib.auth.models import User
from .models import Order
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']



class TradingForm(forms.ModelForm):

        class Meta:
            model = Order
            fields = ['action','quantity','price']
            labels = {'action':'Buy/Sell','quantity':'BTC','price':'BTC Price'}