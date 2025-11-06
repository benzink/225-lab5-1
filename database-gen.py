import sqlite3

conn = sqlite3.connect('data/sample_data.db')
c = conn.cursor()
c.execute("INSERT INTO items (name) VALUES ('Apple'), ('Banana'), ('Carrot')")
conn.commit()
conn.close()
print("Sample data added!")
