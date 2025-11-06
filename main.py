from flask import Flask, render_template
import sqlite3, os

app = Flask(__name__)

DB_PATH = os.path.join("data", "sample_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM items")
    items = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("index.html", items=items)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
