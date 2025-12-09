# app.py
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from scraper import get_stock_data
from database import init_db, add_search, get_history

app = Flask(__name__)
CORS(app)
# Initialize DB when the app starts
init_db()

@app.route("/", methods=["GET"])
def health():
    # Simple health check endpoint (useful for testing EC2)
    return jsonify({"status": "ok", "message": "Stock API is running"})

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Stock Scraper API is running",
        "endpoints": [
            "/api/stock/<ticker>",
            "/api/history",
            "/api/export_csv"
        ]
    })

@app.route("/api/history", methods=["GET"])
def api_history():
    """
    Returns the search history from the database as JSON.
    Format: [
      { "ticker": "...", "price": "...", "change": "...", "timestamp": "..." },
      ...
    ]
    """
    rows = get_history()
    history_list = [
        {
            "ticker": r[0],
            "price": r[1],
            "change": r[2],
            "timestamp": r[3],
        }
        for r in rows
    ]
    return jsonify(history_list)



@app.route("/api/stock/<ticker>", methods=["GET"])
def api_stock(ticker):
    """
    Returns stock data for a given ticker as JSON.
    Also logs the search into the database if successful.
    """
    ticker = ticker.upper()
    data = get_stock_data(ticker)

    # If the scrape worked, save it to history
    if "error" not in data:
        # We only store ticker, price, and change in history
        add_search(data["ticker"], data["price"], data["change"])

    return jsonify(data)

@app.route("/api/export_csv", methods=["GET"])
def export_csv():
    """
    Returns the search history as a downloadable CSV file.
    Angular *can* call this, or you can just use it from the browser.
    """
    rows = get_history()

    # Build rows: header + data
    csv_lines = []
    csv_lines.append(["Ticker", "Price", "Change", "Timestamp"])
    for r in rows:
        csv_lines.append([str(r[0]), str(r[1]), str(r[2]), str(r[3])])

    # Convert to CSV string
    csv_text = "\n".join([",".join(line) for line in csv_lines])

    response = make_response(csv_text)
    response.headers["Content-Disposition"] = "attachment; filename=stock_history.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


if __name__ == "__main__":
    # Required for AWS EC2 deployment
    app.run(host='0.0.0.0', port=5000, debug=True)