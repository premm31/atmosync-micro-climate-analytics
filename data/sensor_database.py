import sqlite3

# Connect to the database (creates it if it doesn't exist)
connection = sqlite3.connect("data/sensor_data.db")

cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_id TEXT,
    temperature REAL,
    humidity REAL,
    vibration REAL,
    timestamp TEXT
)
""")

connection.commit()
connection.close()

print("Database and table created successfully!")