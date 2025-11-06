import sqlite3

conn = sqlite3.connect('data/sample_data.db')
c = conn.cursor()
c.execute("DELETE FROM items")
conn.commit()
conn.close()
print("Database cleared.")
