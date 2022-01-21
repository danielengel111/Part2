from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('query_results', views.query_results, name='query_results'),
    path('buy_stocks', views.buy_stocks, name='buy_stocks'),
]
