import csv
import json
import requests
from collections import OrderedDict
from flask import Flask, render_template, request

app = Flask(__name__)

# Pozyskanie ze strony banku informacji i zapisanie w data_json
response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data_json = response.json()

# Zdefiniowanie listy 'data', w której zawarte są tylko informacje 'currency', 'code', 'bid', 'ask'
for i in data_json:
    data12 = (i.get('rates'))

# Zapiswanie do pliku kantor.csv
with open('kantor.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data12:
        writer.writerow(i)

# Zdefiniowanie listy 'cod', w której zawarte są kody walut
cod = []
for i in data12:
    kod = i.get('code')
    cod.append(kod)

#Zdefiniowanie wyniku przeliczenia waluty jako listę
result = []

@app.route("/waluty/", methods=['GET', 'POST'])
def exchange():
    
    # Wybór kodu waluty, którą chcemy wymienić
    if request.method =='GET':
        items = cod
        return render_template("waluty.html", items=items)
    

    if request.method == 'POST':
        # Pobranie nazwy waluty z listy 'data'
        data = request.form
        currenc = data.get('currency')
        
        # Określenie ilości do przeliczenia
        amoun= data.get('amount')
        amount_num = float(amoun)
        
        # Pobranie 'bid' dla wybranego kodu waluty
        for i in data12:
            if currenc == i.get('code'):
                bi = i.get('bid')
        bid_num = float(bi)

        #Usunięcie poprzedniego wyniku
        result.clear()

        #Przekonwertowanie waluty i wyświetlenie wyniku na kantor.html
        result.append(amount_num/bid_num)
        return render_template("kantor.html", result=result)

# Uruchomienie
if __name__ == '__main__':
    app.run(debug=True)