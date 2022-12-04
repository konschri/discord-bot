import random
import requests
import json
from forex_python.converter import CurrencyRates

def get_response(message: str) -> str:
    p_message = message.lower()
    
    if p_message == "hello":
        return "Hey there!"
    
    if p_message == "roll":
        return str(random.randint(1, 6))
    
    if p_message == "!help":
        return "`This is a dummy help message.`"
    
    return "WUT?"


def get_bitcoin_price(currency):
    currency = currency.upper()
    if currency in ["EUR", "USD", "GBP"]:
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(key)
        data = response.json()
        result = data["price"].split(".")[0]
    
        if currency == "USD":
            return f"`The current price of bitcoin in {currency} is {round(result,2)}`"
        
        c = CurrencyRates()
        if currency == "EUR":
            rate = c.get_rate('USD', 'EUR')
            result = int(result)*rate
        else:
            rate = c.get_rate('USD', 'GBP')
            result = int(result)*rate
        return f"`The current price of bitcoin in {currency} is {round(result,2)}`"
    else:
        return f"`Sorry {currency} is not a valid option. Available options are: EUR USD GBP`"


def get_coin_report():
    url = "http://api.coincap.io/v2/assets/bitcoin/history?=d1"
    headers, payload = {}, {}
    response = requests.request("GET", url, headers=headers, data = payload)
    json_data = json.loads(response.text.encode('utf8'))
    bitcoin_data = json_data["data"]
    return
    


def announce_football_schedule():
    return


