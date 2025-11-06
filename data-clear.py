import sqlite3

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute("DELETE FROM users")
conn.commit()
conn.close()
print("✅ Test data cleared.")
