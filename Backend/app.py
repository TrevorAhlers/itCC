# app.py
from flask import Flask, render_template, request, jsonify
from scraper import get_stock_data
from database import init_db, add_search, get_history

app = Flask(__name__)

# Initialize DB when the app starts
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        data = get_stock_data(ticker)

        # Save valid results to history
        if "error" not in data:
            add_search(data["ticker"], data["price"], data["change"])
    return render_template("index.html", data=data)


@app.route("/history")
def history():
    entries = get_history()
    return render_template("history.html", history=entries)


@app.route("/api/<ticker>")
def api_ticker(ticker):
    ticker = ticker.upper()
    data = get_stock_data(ticker)
    return jsonify(data)


if __name__ == "__main__":
    # Required for AWS EC2 deployment
    app.run(host='0.0.0.0', port=5000, debug=True)