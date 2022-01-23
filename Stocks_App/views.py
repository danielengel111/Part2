from django.shortcuts import render
from django.db import connection
from datetime import datetime


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def home(request):
    return render(request, 'home.html')


def get_last_transactions():
    with connection.cursor() as cursor:
        cursor.execute("""
     SELECT tDate as date, ID as investor_id, TQuantity as quantity
     FROM Transactions
     order by date desc, ID desc;
     """)
        return dictfetchall(cursor)[0:10]


def id_exists(id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
     SELECT *
     FROM Investor
     WHERE ID = {id};
     """)
        if not dictfetchall(cursor):
            return False
        return True


def add_transaction_page(request):
    table_results = get_last_transactions()
    return render(request, 'add_transaction.html',
                  {'table_results': table_results, 'error_message': ""})


def write_transaction(ID, transaction_sum, today):
    with connection.cursor() as cursor:
        cursor.execute(f"""
     UPDATE Investor
     SET AvailableCash = AvailableCash + {transaction_sum}
     WHERE ID = {ID};
     """)
        cursor.execute(f"""
     INSERT INTO Transactions (tDate, ID, TQuantity)
     VALUES ('{today}', {ID}, {transaction_sum});
     """)


def delete_today_transaction(ID, today):
    with connection.cursor() as cursor:
        cursor.execute(f"""
             SELECT *
             FROM Transactions
             WHERE tDate = '{today}' AND ID = {ID};
             """)
        today_trans = dictfetchall(cursor)
        if not today_trans:
            return
        today_trans = today_trans[0]
        cursor.execute(f"""
             UPDATE Investor
             SET AvailableCash = AvailableCash - {today_trans['TQuantity']}
             WHERE ID = {ID};
             """)
        cursor.execute(f"""
             DELETE
             FROM Transactions
             WHERE tDate = '{today}' AND ID = {ID};
             """)


def add_transaction(request):
    error_message = ""
    if request.method == 'POST' and request.POST:
        ID = request.POST['id']
        transaction_sum = request.POST['transaction_sum']
        today = datetime.today().strftime('%Y-%m-%d')
    if not id_exists(ID):
        error_message = "Investor ID doesn't exist"
    else:
        delete_today_transaction(ID, today)
        write_transaction(ID, transaction_sum, today)

    table_results = get_last_transactions()
    return render(request, 'add_transaction.html',
                  {'table_results': table_results, 'error_message': error_message})


def query_results(request):
    return render(request, 'query_results.html')


def get_last_purchases():
    with connection.cursor() as cursor:
        cursor.execute("""
     SELECT Buying.tDate as date, ID as investor_id, Buying.Symbol as company, round(Price * BQuantity, 2) as payed
     FROM Buying
     inner join
     Stock 
     on Buying.Symbol = Stock.Symbol and Buying.tDate = Stock.tDate
     order by payed desc, ID desc;
     """)
        return dictfetchall(cursor)[0:10]


def company_exists(symbol):
    with connection.cursor() as cursor:
        cursor.execute(f"""
     SELECT *
     FROM Company
     WHERE Symbol = '{symbol}';
     """)
        if not dictfetchall(cursor):
            return False
        return True


def enough_cash(ID, amount):
    with connection.cursor() as cursor:
        cursor.execute(f"""
             SELECT *
             FROM Investor
             WHERE ID = {ID};
             """)
        investor = dictfetchall(cursor)[0]
    cash = investor['AvailableCash']
    if cash < amount:
        return False
    return True


def update_stock(symbol, today):
    with connection.cursor() as cursor:
        cursor.execute(f"""
             SELECT *
             FROM Stock
             WHERE Symbol = '{symbol}'
             ORDER BY tDate DESC;
             """)
        stock = dictfetchall(cursor)[0]
        price = stock['Price']
        last_date = str(stock['tDate'])
        if today != last_date:
            cursor.execute(f"""
                INSERT INTO Stock (Symbol, tDate, Price)
                VALUES ('{symbol}', '{today}', {price});
                """)
        return price


def buy_stocks(request):
    error_message = ""
    if request.method == 'POST' and request.POST:
        ID = request.POST['id']
        company = request.POST['company']
        quantity = int(request.POST['quantity'])
        today = datetime.today().strftime('%Y-%m-%d')

    condition1 = id_exists(ID)
    condition2 = company_exists(company)
    if not condition1 and condition2:
        error_message = "Investor ID doesn't exist"
    elif condition1 and not condition2:
        error_message = "Company Symbol doesn't exist"
    elif not condition1 and not condition2:
        error_message = "Investor ID doesn't exist and Company Symbol doesn't exist"
    else:
        price = update_stock(company, today)
        if not enough_cash(ID, price * quantity):
            error_message = "Not enough money for payment."
        else:
            pass

    table_results = get_last_purchases()
    return render(request, 'buy_stocks.html',
                  {'table_results': table_results, 'error_message': error_message})


def buy_stocks_page(request):
    table_results = get_last_purchases()
    return render(request, 'buy_stocks.html',
                  {'table_results': table_results, 'error_message': ""})
