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

def transac_rec(symbol,price,shares,username,direction):
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..", f"users/{username}", f"{username}.csv")
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..", f"users/{username}", f"{username}_transactions.csv")
    with open(csv_file_path, "a+",newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
        writer.writerow({"Stock": symbol, "Bought Price": price, "Current Price": price, "Shares": shares, "Total Value": price*shares, "Unrealized Gain/Loss": "0"})
    with open(csv_file_path2, "a+",newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Transaction", "Value"])
        if direction == "Buy":
            writer.writerow({"Transaction": f"Bought {shares} Shares of {symbol}", "Value": shares*price*-1})
        else:
            writer.writerow({"Transaction": f"Sold {shares} Shares of {symbol}", "Value": shares*price})

   
