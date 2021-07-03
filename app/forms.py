from django import forms
from django.contrib.auth.models import User
from .models import Order,Profile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']



class TradingForm(forms.ModelForm):

    # override the __init__ function to unpack the request object from the kwargs.
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(TradingForm,self).__init__(*args,**kwargs)
        # specify Queryset inside the __init__ function
        self.fields['profile'].queryset = Profile.objects.filter(user=self.request.user)

    class Meta:
        model = Order
        fields = ['profile','action','quantity','price']
        labels = {'action':'Buy/Sell','quantity':'BTC','price':'BTC Price'}