from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def add_transaction(request):
    return render(request, 'add_transaction.html')


def query_results(request):
    return render(request, 'query_results.html')


def buy_stocks(request):
    return render(request, 'buy_stocks.html')
