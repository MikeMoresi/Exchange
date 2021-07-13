from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='app/registration/login.html')),
    path('placeOrders/',views.placeOrders,name='placeOrders'),
    path('openOrders/',views.openOrders, name='openOrders'),
    path('profitLoss/', views.profitLoss, name='profitLoss'),
]