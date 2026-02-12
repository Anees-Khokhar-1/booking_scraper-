from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_all_data():
    conn = sqlite3.connect("scrap_data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM scrap_data")
    rows = cur.fetchall()

    conn.close()
    return rows

@app.route("/")
def home():
    data = get_all_data()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)