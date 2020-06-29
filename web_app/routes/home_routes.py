from flask import Blueprint, render_template, redirect, request, flash
from dotenv import load_dotenv
import csv
import os
import pandas as pd 

from app.login import login_auth
from app.signup import signup
from app.active_user import active_user
from app.active_user import clear_user
from app.login import create_folder
from app.live_price import live_price
from app.live_price import transac_rec
from app.live_price import update_prices

def to_usd(my_price):
    return f"${my_price:,.2f}"

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    clear_user()
    return render_template("home.html")

@home_routes.route("/about")
def about():
    return render_template("about.html")

@home_routes.route("/buy-sell")
def buy_sell():
    return render_template("buy_sell.html")

@home_routes.route("/transactions")
def transac():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    return render_template("transactions.html", results=results)

@home_routes.route("/register")
def register():
    return render_template("new_user_form.html")

@home_routes.route("/dashboard", methods=["GET"])
def dashboard():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    results = pd.read_csv(csv_file_path).to_dict("records")
    if len(results) == 0:
        results = ""
    stocks_df = pd.read_csv(csv_file_path)
    transactions_df = pd.read_csv(csv_file_path2)
    cash_value = float(transactions_df["Value"].sum())
    positions = stocks_df["Total Value"].sum()
    if positions == " ":
        positions = 0.00
        total = cash_value
    else:
        positions = float(positions)
        total = cash_value + positions
    return render_template("dashboard.html", username=username, results=results, value=to_usd(cash_value), value2=to_usd(positions), value3=to_usd(total))

@home_routes.route("/users/login", methods=["POST"])
def check_user():
    user = dict(request.form)
    if user['username'] == "" or user['password'] == "":
        flash(f"Invalid Entry", "danger")
        return redirect("/")
    else:
        username = user['username']
        password = user['password']
        login_status = login_auth(username,password)
        if str(login_status) == "Username/Password Incorrect":
            flash(f"{login_status}", "danger")
            return redirect("/")
        else:
            create_folder(username)
            flash(f"{login_status}", "success")
            return redirect("/dashboard")

@home_routes.route("/users/create", methods=["POST"])
def create_user():
    user = dict(request.form)
    if user['email'] == "" or user['username'] == "" or user['password'] == "":
        flash(f"Invalid Entry", "danger")
    elif not "@" in user['email'] or not "." in user['email']:
        flash(f"Invalid Email", "danger")
    else:
        results = signup(user['email'],user['username'],user['password'])
        if str(results) == "Username Is Already Taken" or str(results) == "Already Account Associated With That Email":
            flash(f"{results}", "danger")
        else:
            flash(f"{results}", "success")
    return redirect("/")

@home_routes.route("/users/buy", methods=["POST"])
def buy_order():
    user = dict(request.form)
    username = active_user()
    results = live_price(user['ticker'],API_KEY)
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    pos_count = len(pd.read_csv(csv_file_path).to_dict("records"))
    csv_file_path2 = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}_transactions.csv")
    data = pd.read_csv(csv_file_path).to_dict("records")
    transactions_df = pd.read_csv(csv_file_path2)
    cash_value = float(transactions_df["Value"].sum())
    stock = [n["Stock"] for n in data if n["Stock"] == user['ticker']]
    if str(results) == "Invalid Stock Symbol, Try Again":
        flash(f"{results}", "danger")
    elif len(stock) > 0:
        shares = int(user['share_count'])
        if (shares*results) > cash_value:
            flash(f"Insufficient Funds", "danger")
        else:
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
            flash(f"You Bought {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
            transac_rec(user['ticker'],results,shares,username,"Buy+")
    elif pos_count > 4:
        flash(f"Reached Positions Limit of 5, Please Sell Position Before Buying A New One", "danger")
    else:
        shares = int(user['share_count'])
        if (shares*results) > cash_value:
            flash(f"Insufficient Funds", "danger")
        else:   
            flash(f"You Bought {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
            transac_rec(user['ticker'],results,shares,username,"Buy")
    return redirect("/buy-sell")

@home_routes.route("/users/sell", methods=["POST"])
def sell_order():
    username = active_user()
    csv_file_path = os.path.join((os.path.dirname(__file__)),"..","..", f"users/{username}", f"{username}.csv")
    data = pd.read_csv(csv_file_path).to_dict("records")
    user = dict(request.form)
    stock = [n["Stock"] for n in data if n["Stock"] == user['ticker']]
    shares_aval = [n["Shares"] for n in data if n["Stock"] == user['ticker']]
    if not stock:
        flash(f"You Do Not Own That Stock", "danger")
    elif int(user['share_count']) > shares_aval[0]:
        flash(f"You Do Not Own That Many Shares", "danger")
    else:
        results = live_price(user['ticker'],API_KEY)
        if str(results) == "Invalid Stock Symbol, Try Again":
            flash(f"{results}", "danger")
        else:
            shares = int(user['share_count'])
            with open(csv_file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                lines = []
                for row in reader:
                    if stock[0] != row["Stock"]:
                        lines.append(row)
                    elif shares_aval[0] > int(user['share_count']):
                        row["Shares"] = int(row["Shares"]) - int(user['share_count'])
                        row["Total Value"] = int(row["Shares"]) * float(row["Current Price"])
                        lines.append(row)
            with open(csv_file_path, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
                writer.writeheader()
                writer.writerows(lines)
            transac_rec(user['ticker'],results,shares,username,"Sell")
            flash(f"You Sold {shares} Shares of {user['ticker']} For {to_usd(results*shares)}", "success")
    return redirect("/buy-sell")

@home_routes.route("/users/update")
def update():
    username = active_user()
    update_prices(username,API_KEY)
    flash(f"Market Values Updated", "success")
    return redirect("/dashboard")

@home_routes.route("/logout")
def logout():
    flash(f"You Have Succesfully Logged Out", "success")
    clear_user()
    return redirect("/")
