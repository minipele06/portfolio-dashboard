from dotenv import load_dotenv
import os
import requests
import csv
import pandas as pd
import json

def live_price(symbol,API_KEY):
    try:
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
    except KeyError:
        return "Invalid Stock Symbol, Try Again"


def transac_rec(symbol,price,shares,username,direction):
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..", f"users/{username}", f"{username}.csv")
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..", f"users/{username}", f"{username}_transactions.csv")
    if direction == "Buy":
        with open(csv_file_path, "a+",newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
            writer.writerow({"Stock": symbol, "Bought Price": f"{price:.2f}", "Current Price": f"{price:.2f}", "Shares": int(shares), "Total Value": format((price*shares),".2f"), "Unrealized Gain/Loss": "0"})
        with open(csv_file_path2, "a+",newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Transaction", "Value"])
            writer.writerow({"Transaction": f"Bought {shares} Shares of {symbol}", "Value": shares*price*-1})
    elif direction == "Buy+":
        with open(csv_file_path2, "a+",newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Transaction", "Value"])
            writer.writerow({"Transaction": f"Bought {shares} Shares of {symbol}", "Value": shares*price*-1})
    else:
        with open(csv_file_path2, "a+",newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Transaction", "Value"])
            writer.writerow({"Transaction": f"Sold {shares} Shares of {symbol}", "Value": shares*price})

def update_prices(username, API_KEY):
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..", f"users/{username}", f"{username}.csv")
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        lines = []
        for row in reader:
            row["Current Price"] = float(live_price(row["Stock"], API_KEY))
            row["Total Value"] = int(row["Shares"]) * float(row["Current Price"])
            row["Unrealized Gain/Loss"] = (float(row["Current Price"]) - float(row["Bought Price"])) * int(row["Shares"])
            lines.append(row)
    with open(csv_file_path, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
                writer.writeheader()
                writer.writerows(lines)

def buy_transac(csv_file_path,stock,shares,results):
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        lines = []
        for row in reader:
            if stock[0] != row["Stock"]:
                lines.append(row)
            else:
                row["Shares"] = int(row["Shares"]) + shares
                row["Total Value"] = float(row["Total Value"]) + (results*shares)
                row["Bought Price"] = float(row["Total Value"])/float(row["Shares"])
                lines.append(row)
    with open(csv_file_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
        writer.writeheader()
        writer.writerows(lines)

def sell_transac(csv_file_path,stock,shares,results,shares_aval):
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        lines = []
        for row in reader:
            if stock[0] != row["Stock"]:
                lines.append(row)
            elif shares_aval > shares:
                row["Shares"] = int(row["Shares"]) - shares
                row["Total Value"] = int(row["Shares"]) * float(row["Current Price"])
                lines.append(row)
    with open(csv_file_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
        writer.writeheader()
        writer.writerows(lines)