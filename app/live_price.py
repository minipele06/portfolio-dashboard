from dotenv import load_dotenv
import os
import requests
import csv
import pandas as pd
import json

def live_price(symbol,API_KEY):
    if symbol.isalpha() == False:
        return "Invalid Stock Symbol, Try Again"
    elif len(symbol) > 4:
        return "Invalid Stock Symbol, Try Again"
    elif symbol == "":
        return "Invalid Stock Symbol, Try Again"
    else:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        raw_data = json.loads(response.text)
        return float(raw_data["Global Quote"]["05. price"])