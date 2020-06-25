import csv
import os

def active_user():
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "users", "active_user.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            result = row["Username"]
            return result

def clear_user():
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "users", "active_user.csv")
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Username", "Email"])
        writer.writerow({"Username": "", "Email": ""})
        