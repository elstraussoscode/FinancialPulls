from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

api_key = "488e36aa315e7ad8733d7bca99eb5553"

companies = ["AAPL", "BABA"]

# Fetch the Data and create a Dictionary for each stock because the API does not send the ticker symbol
def fetch_data():
    financial_statements = {}
    for company in companies:
        res = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{company}?apikey={api_key}")
        data = res.json()
        financial_statements[company]=data

    return financial_statements

stocks = fetch_data()

# Makes Json Pretty
#print(json.dumps(stocks, sort_keys=True, indent=4))

for stock in stocks:
    # prints the top level key
    print(stock)
    # prints the PE Ratio
    print(stocks[stock][0]["peRatioTTM"])

@app.route("/")
def home():
    return render_template("tables.html", stocks = stocks)

if __name__ == '__main__':
    app.run()