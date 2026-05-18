import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Create connection
conn = sqlite3.connect("database/churn.db")

# Save table
df.to_sql(
    "churn_data",
    conn,
    if_exists="replace",
    index=False
)

# Verify table created
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print("Tables:", cursor.fetchall())

print("Database created successfully!")

conn.close()