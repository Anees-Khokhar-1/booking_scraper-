import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv(r"D:\booking_scraper\output\Pakistan.csv")

# Connect DB
conn = sqlite3.connect(r"D:\booking_scraper\scrap_data.db")

# Insert CSV into EXISTING table
df.to_sql("scrap_data", conn, if_exists="append", index=False)

conn.close()

print("CSV successfully imported into SQLite!")