from django.urls import path
from . import views
from .views import Trading
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='app/registration/login.html')),
    path('trading/',Trading.as_view(template_name='app/trading.html',success_url='/openOrders')),
    path('openOrders/',views.openOrders, name='openOrders'),
    path('profit/', views.profitLoss, name='profit'),
]