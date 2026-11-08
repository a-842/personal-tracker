import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

cursor.execute("""



""")

print(cursor.fetchall())

conn.commit()