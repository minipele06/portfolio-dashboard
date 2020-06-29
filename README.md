# Stock Market Simulator

## Functionality

This web app allows you to purchase and hold stocks (up to 5 at any one time) and track your performance over time. The following information will be tracked

* Purchase Price
* Current Price
* Total Value of Stocks
* Unrealized Gain/Loss
* Total Value of Cash
* Total Account Value
* Transaction History

## Setup

### Repo Setup
Use [GitHub](https://github.com/minipele06/portfolio-dashboard) to clone the project repository for the Stock Market Simulator. Use GitHub Desktop software or the command-line to download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line:

>cd ~/Desktop/portfolio-dashboard

### Environment Setup
Create and activate a new Anaconda virtual environment:

>conda create -n portfolio-env python=3.7 # (first time only)

>conda activate portfolio-env

From within the virtual environment, install the required packages specified in the "requirements.txt" file:

>pip install -r requirements.txt

### AlphaVantage Setup
The program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co/). Follow the link and signup for an account which will then issue you your individual API Key. You will then need to create a .env file to save your environment variable which should be labeled ALPHAVANTAGE_API_KEY.

>ALPHAVANTAGE_API_KEY="abc123"

## Instructions
From within the virtual environment, demonstrate your ability to run the web app from the command-line:

Mac
>FLASK_APP=web_app flask run

PC

If you receive a message stating the following:

>Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Then you have succesfully launched the web app. Go to you internet browser and enter the above address to access the app locally. If you would like to run this web app on an external server, you may do so through a host of different servers. Check out Professor Rossetti's page explaining in further detail how to proceed. 

## Step-by-Step Guide

As stated above, once you receive a message in your terminal that the web app is running locally, you may then navigate to the local address.

### Home Page

The home page is the main landing page where it explains the basics of the web application and has a link to an about page which delves in to what needs the application is trying to meet.

#### Register

The registration box allows users who have never used the app to create an account.

* Email: An email is required to start your account. The program will validate that the provided email address includes an "@" symbol.

* Username: You may enter any username that you would like. However, duplicate usernames will not be permitted.

* Password: There are no password requirements other than there must be at least one character and can not be blank.

If any of the fields are empty, the program will give you an error message.

#### Login

The login box will authenticate users credentials. On a succesful authorization, users will be taken to their dashboard page.

If any of the fields are empty, the program will give you an error message.

The forgot password button is not currently functional and will only flash a warning message.

### About Page

The about page quickly delves in to the user needs that the program is intending to fulfill. 

### Dashboard

### Buy/Sell

### Transactions

### Logout
As stated above, once you receive a message to enter your stock symbol, you are ready to use the program. 

You may enter as many stock tickers as you'd like (depending on the API Key, the free version allows you to pull 5 stocks per minute or 500 per day). Once you've completed entering in your desired symbols, type 'Done' the next time the program prompts you to enter a symbol. Your symbols will be validated to exclude alphanumeric inputs and inputs greater than 4 characters.

Once you have entered 'Done', the program will proceed to pull the corresponding data. If any symbols do not exist, the program will notify you.

Finally, the program will notify you of the information outlined in the functionality section.

## Quality

The below screenshot shows the results of running the code through Code Climate in order to test the simplicity and maintainability of the code

![Image of Code Climate](/codeclimate.png)

## Minimum Viable Product