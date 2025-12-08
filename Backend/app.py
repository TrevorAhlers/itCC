# app.py
import csv
from flask import Flask, render_template, request, jsonify, make_response
from scraper import get_stock_data
from database import init_db, add_search, get_history
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
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

@app.route("/export_csv")
def export_csv():
    history = get_history()

    # create CSV in memory
    si = []
    si.append(["Ticker", "Price", "Change", "Timestamp"])

    for row in history:
        si.append(list(row))

    # return CSV file to user
    response = make_response("\n".join([",".join(map(str, s)) for s in si]))
    response.headers["Content-Disposition"] = "attachment; filename=stock_history.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

if __name__ == "__main__":
    # Required for AWS EC2 deployment
    app.run(host='0.0.0.0', port=5000, debug=True)