import sqlite3

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute("INSERT INTO users (name) VALUES ('Alice')")
c.execute("INSERT INTO users (name) VALUES ('Bob')")
conn.commit()
conn.close()
print("✅ Test data generated.")
