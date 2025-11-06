from flask import Flask
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Hello from Flask CI/CD!"

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)
