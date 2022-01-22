from django.shortcuts import render
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def home(request):
    return render(request, 'home.html')


def add_transaction(request):
    with connection.cursor() as cursor:
        cursor.execute("""
     SELECT tDate as date, ID as investor_id, TQuantity as quantity
     FROM Transactions
     order by date desc, ID desc
     """)
        table_results = dictfetchall(cursor)[0:10]
    return render(request, 'add_transaction.html', {'table_results': table_results})


def query_results(request):
    return render(request, 'query_results.html')


def buy_stocks(request):
    with connection.cursor() as cursor:
        cursor.execute("""
     SELECT Buying.tDate as date, ID as investor_id, Buying.Symbol as company, round(Price * BQuantity, 2) as payed
     FROM Buying
     inner join
     Stock 
     on Buying.Symbol = Stock.Symbol and Buying.tDate = Stock.tDate
     order by payed desc, ID desc
     """)
        table_results = dictfetchall(cursor)[0:10]
    return render(request, 'buy_stocks.html', {'table_results': table_results})
