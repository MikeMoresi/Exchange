from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ObjectIdField
from django.db.models import Q
from django.http import JsonResponse
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

    def checkOrders(self):

        #BUY ORDER

        #check if there are or no LTE Sell Orders from other accounts
        sellOrders = Order.objects.filter((~Q(profile_id=self.profile)),done='False',action='sell',price__lte = self.price).order_by('price')
        if not sellOrders:
            return JsonResponse('at this moment there aren t sell orders to satisfy your request, we saved your order on our trading book.',safe=False)
        else:
            #find the cheapest sell open order
            cheapSellOrder = sellOrders[0]
            print(cheapSellOrder)

            #change order status from False to True
            cheapSellOrder.done = 'True'
            cheapSellOrder.save(update_fields=['done'])
            self.done = 'True'

            #modify account's Profile fields
            #nBTC
            cheapSellOrder.profile.nBTC -= cheapSellOrder.quantity
            cheapSellOrder.profile.save(update_fields=['nBTC'])
            self.profile.nBTC += self.quantity
            self.profile.save(update_fields=['nBTC'])
            #wallet
            cheapSellOrder.profile.wallet = cheapSellOrder.profile.nBTC*btcValue()
            cheapSellOrder.profile.save(update_fields=['wallet'])
            self.profile.wallet = self.profile.nBTC*btcValue()
            self.profile.save(update_fields=['wallet'])
            #profitLoss
            cheapSellOrder.profile.profitLoss += cheapSellOrder.price
            cheapSellOrder.profile.save(update_fields=['profitLoss'])
            self.profile.profitLoss -= self.price
            self.profile.save(update_fields=['profitLoss'])





