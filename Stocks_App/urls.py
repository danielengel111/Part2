from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('add_transaction_page', views.add_transaction_page, name='add_transaction_page'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('query_results', views.query_results, name='query_results'),
    path('buy_stocks_page', views.buy_stocks_page, name='buy_stocks_page'),
    path('buy_stocks', views.buy_stocks, name='buy_stocks'),
]
