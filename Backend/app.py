# app.py
import csv
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, make_response
from scraper import get_stock_data
from database import init_db, add_search, get_history
import os
from datetime import datetime
import json



app = Flask(__name__)
CORS(app)
# Initialize DB when the app starts
init_db()
HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

with open(HISTORY_FILE, "r") as f:
    history = json.load(f)

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = []


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        ticker = request.form["ticker"].upper()
        data = get_stock_data(ticker)

        
        if "error" not in data:
            add_search(data["ticker"], data["price"], data["change"],data["day_range"],data["volume"])
    return render_template("index.html", data=data)



@app.route("/history/json")
def get_history():
    return jsonify(history)

@app.route("/api/history")
def api_history():
    rows = get_history()

    history_list = []
    for r in rows:
        history_list.append({
            "ticker": r[0],
            "price": r[1],
            "change": r[2],
            "Day Range": r[3],
            "Volume": r[4],
            "timestamp": r[5]
        })

    return jsonify(history_list)


@app.route("/api/<ticker>")
def api_ticker(ticker):
    ticker = ticker.upper().strip()
    data = get_stock_data(ticker)

    if "error" not in data:
        
        data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append(data)

        
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

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