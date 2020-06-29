import csv
import os


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