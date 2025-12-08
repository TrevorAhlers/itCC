import yfinance as yf

def get_stock_data(ticker: str):
    ticker = ticker.upper().strip()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Check if info is valid
        if not info or "regularMarketPrice" not in info:
            return {"error": f"Invalid ticker or no data found for '{ticker}'"}

        return {
            "ticker": ticker,
            "price": info.get("regularMarketPrice", "N/A"),
            "change": info.get("regularMarketChangePercent", "N/A"),
            "day_range": f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
            "volume": info.get("volume", "N/A"),
        }

    except Exception as e:
        return {"error": f"Could not retrieve data for '{ticker}': {e}"}


