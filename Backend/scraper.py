import requests
from bs4 import BeautifulSoup

def get_stock_data(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        # price + change
        price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
        change = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"}).text

        # Day's Range
        day_range_label = soup.find("td", string="Day's Range")
        day_range = day_range_label.find_next("td").text if day_range_label else "N/A"

        # Volume
        volume_label = soup.find("td", string="Volume")
        volume = volume_label.find_next("td").text if volume_label else "N/A"

        return {
            "ticker": ticker,
            "price": price,
            "change": change,
            "day_range": day_range,
            "volume": volume
        }

    except Exception:
        return {"error": f"Could not retrieve data for {ticker}"}
