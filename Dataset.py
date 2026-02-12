import sqlite3

conn = sqlite3.connect("scrap_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scrap_data(
    No INTEGER PRIMARY KEY AUTOINCREMENT,
    Hotel TEXT,
    Location TEXT,
    Price TEXT,
    Rating REAL
)
""")

conn.commit()
conn.close()

print("Table created successfully")