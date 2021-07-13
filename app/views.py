from django.shortcuts import render,redirect
from .forms import RegistrationForm, TradingForm
from .models import Profile,Order
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


def placeOrders(request):

    if request.method == "POST":
        form = TradingForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.profile = Profile.objects.filter(user=request.user)[0]
            order.checkOrders()
            order.save()
            return redirect('/openOrders', pk=order.pk)
    else:
        form = TradingForm()
    return render(request, 'app/trading.html', {'form': form})



def openOrders(request):
    response = []
    opOrders = Order.objects.filter(done='False')
    for data in opOrders:
        response.append(
            {
                'price': data.price,
                'action': data.action
            }
        )

    # save ip address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    currentUser = Profile.objects.filter(user=request.user)[0]
    currentUser.ips.append(ip)
    currentUser.save(update_fields=['ips'])

    return JsonResponse(response, safe=False)

#function to show user profit-loss
def profitLoss(request):
    response = []
    currentUser = Profile.objects.filter(user=request.user)
    for data in currentUser:
        response.append(
            {
                'profitLoss':data.profitLoss
            }
        )
    return JsonResponse(response,safe=False)





