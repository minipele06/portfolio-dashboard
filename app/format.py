#formatting functions

#format to USD with two decimals
def to_usd(my_price):
    return f"${my_price:,.2f}"

#formatting dashboard csv dictionary
def format_dict(results):
    for row in results:
        row["Bought Price"] = to_usd(float(row["Bought Price"]))
        row["Current Price"] = to_usd(float(row["Current Price"]))
        row["Total Value"] = to_usd(float(row["Total Value"]))
        row["Unrealized Gain/Loss"] = to_usd(float(row["Unrealized Gain/Loss"]))

#formatting transaction history dictionary
def format_dict2(results):
    for row in results:
        row["Value"] = to_usd(float(row["Value"]))
