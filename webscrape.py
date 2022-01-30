import bs4
import requests

res = requests.get("https://companiesmarketcap.com/china/largest-companies-in-china-by-market-cap/")
soup = bs4.BeautifulSoup(res.text, "html.parser")

stocks = soup.find_all("div", {"class": "company-code"})
ticker_list = []
for stock in stocks:
    ticker = stock.get_text()
    ticker_list.append(ticker)
print(ticker_list)