from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
FILE = "expenses.json"

def load():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

@app.route("/")
def index():
    expenses = load()
    total = sum(float(e["amount"]) for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        expenses = load()
        expenses.append({"amount": amount, "category": category})
        save(expenses)
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/delete/<int:index>")
def delete(index):
    expenses = load()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save(expenses)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)