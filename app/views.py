from django.shortcuts import render,redirect
from .forms import RegistrationForm, TradingForm
from .models import Profile,Order
from pymongo import MongoClient
from bson.json_util import dumps
from django.views import generic
from django.http import JsonResponse


# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            return redirect('/login')
    else:
        form = RegistrationForm()
    return render(request, 'app/registration.html',{'form':form })


class Trading(generic.CreateView):
    model = Order
    form_class = TradingForm
    template_name = 'app/trading.html'

    def get_form_kwargs(self):
        # Passes the request object to the form class
        kwargs = super(Trading,self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs




    def orderCheck(self,request):

        # connect to MongoDB, engine
        client = MongoClient('localhost', 27017)
        db = client.engine
        collectionOrder = db.app_order
        collectionProfile = db.app_profile

        # get user IP and save it
        current_user = request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        newIP = {'$push': {'ips': ip}}
        collectionProfile.update_one({'user_id': current_user}, newIP)


        #BUY ORDER

        # count sell open orders to verify if there are or no
        pipelineSell = [{
            '$match': {
                'done': 'False',
                'action': 'sell'
            }}, {
            '$group': {'_id': 'action', 'count': {'$sum': 1}}
        }
        ]
        result = collectionOrder.aggregate(pipelineSell)
        for doc in result:
            docSell = doc['count']


        if (docSell != 0):

            # select a buy order with a price greater than or equal to the sell order
            sellOrder = collectionOrder.find_one({'action': 'sell', 'done': 'False'})
            buyOrder = collectionOrder.find_one({'profile_id':{'$eq':current_user.id},'action': 'buy', 'done': 'False', 'price': {'$gte': sellOrder['price']}})
            # change from false to true order status
            orderDone = {'$set': {'done': 'True'}}
            collectionOrder.update_one(buyOrder, orderDone)
            collectionOrder.update_one(sellOrder, orderDone)
            # modify numbers of BTC
            buyer = collectionProfile.find_one({'user_id': {'$eq': buyOrder['profile_id']}})
            # the are no fees transaction
            fees = 0
            newNBTC = {'$inc': {'nBTC': buyer['quantity']-fees}}
            collectionProfile.update_one(buyer, newNBTC)
            # modify profit-loss field
            newProfit = {'$inc': {'profitLoss': -(buyer['price'])}}
            collectionProfile.update_one(buyer, newProfit)

        else:
            JsonResponse('There is no sell order to satisfy your request. Retry later',safe=False)


        #SELL ORDER

            # count buy open orders to verify if there are or no
            pipelineSell = [{
                '$match': {
                    'done': 'False',
                    'action': 'buy'
                }}, {
                '$group': {'_id': 'action', 'count': {'$sum': 1}}
            }
            ]
            result = collectionOrder.aggregate(pipelineSell)

        for doc in result:
                docBuy = doc['count']

        if (docBuy != 0):

            # select a sell order with a price less than or equal to the buy order
            sellOrder = collectionOrder.find_one({'action': 'buy', 'done': 'False'})
            buyOrder = collectionOrder.find_one({'profile_id': {'$eq': current_user.id}, 'action': 'sell', 'done': 'False','price': {'$lte': sellOrder['price']}})
            orderDone = {'$set': {'done': 'True'}}
            # change from false to true order status
            collectionOrder.update_one(buyOrder, orderDone)
            collectionOrder.update_one(sellOrder, orderDone)
            # modify numbers of BTC
            seller = collectionProfile.find_one({'user_id': {'$eq': sellOrder['profile_id']}})
            # the are no fees transaction
            fees = 0
            newNBTC = {'$inc': {'nBTC': -((seller['quantity'])-fees)}}
            collectionProfile.update_one(seller, newNBTC)
            # modify profit-loss field
            newProfit = {'$inc': {'profitLoss': seller['price']}}
            collectionProfile.update_one(seller, newProfit)

        else:
            JsonResponse('There is no buy order to satisfy your request. Retry later',safe=False)


#function to show all open orders
def openOrders(request):
    client = MongoClient('localhost', 27017)
    db = client.engine
    collectionOrder = db.app_order
    s = collectionOrder.find({'done': 'False'},{'_id':0,'id':1,'price':1,'action':1})
    sList = list(s)
    jsonData = dumps(sList)
    return JsonResponse(jsonData, safe=False)


#function to show user profit-loss
def profitLoss(request):
    client = MongoClient('localhost', 27017)
    db = client.engine
    current_user = request.user
    collectionProfile = db.app_profile
    profile = collectionProfile.find_one({'user_id': {'$eq': current_user.id}},{'_id':0,'id':1,'profitLoss':1})
    profileList = list(profile)
    jsonData = dumps(profileList)
    return JsonResponse(jsonData, safe=False)




