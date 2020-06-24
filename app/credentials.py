import csv
import pandas as pd 
import os

def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)

username = input("Please Enter Your Username: ")
password = input("Please Enter Your Password: ")

csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")

with open(csv_filepath, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row["Username"] == str(username):
            print("Username Is Already Taken")
            exit()

with open(csv_filepath, "a+",newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["Username", "Password"])
    writer.writerow({"Username": username, "Password": password})

