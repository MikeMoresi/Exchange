from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ObjectIdField

import random
#import btc value from CoinMarketCap
from .cripto_values import btcValue

# Create your models here.

class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    ips = models.Field(default=[])
    subprofiles = models.Field(default={})
    n = random.randint(1,10)
    nBTC = models.IntegerField(default=n)
    #after signup assign a random number of BTC
    wallet = models.FloatField(default=btcValue()*n)
    profitLoss = models.FloatField(default=0)


buy_sell_choise= [('buy','Buy'),('sell','Sell')]


class Order(models.Model):
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=btcValue())
    action = models.Field(choices=buy_sell_choise)
    quantity = models.FloatField()
    done = models.CharField(default='False',max_length=100)



