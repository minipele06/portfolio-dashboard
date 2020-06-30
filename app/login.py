import csv
import os

#authenticates user login
def login_auth(username,password):
    csv_filepath = os.path.join((os.path.dirname(__file__)),"..", "credentials", "u&p.csv")
    with open(csv_filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Username"] == str(username) and row["Password"] == str(password):
                csv_filepath2 = os.path.join((os.path.dirname(__file__)),"..", "users", "active_user.csv")
                with open(csv_filepath2, "w") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=["Username", "Email"])
                    writer.writeheader()
                    writer.writerow({"Username": username, "Email": row["Email"]})
                result = "Logged In"
                return result
    result = "Username/Password Incorrect"
    return result

#creates user folders when first registering
def create_folder(username):
    isexist = os.path.exists(os.path.join((os.path.dirname(__file__)),"..",f"users/{username}"))
    if isexist == False:
        path = os.path.join((os.path.dirname(__file__)),"..",f"users/{username}")
        os.mkdir(path) 
        with open(f"{path}/{username}.csv", 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["Stock", "Bought Price", "Current Price", "Shares", "Total Value", "Unrealized Gain/Loss"])
            writer.writeheader()
        with open(f"{path}/{username}_Transactions.csv", 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["Transaction", "Value"])
            writer.writeheader()
            writer.writerow({"Transaction": "Initial Funding", "Value": "100000"})
