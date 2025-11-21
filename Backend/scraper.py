# scraper.py
import requests
from bs4 import BeautifulSoup

def get_stock_data(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
        change = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"}).text
        return {"ticker": ticker, "price": price, "change": change}
    except:
        return {"error": "Could not retrieve data"}
