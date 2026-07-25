import sqlite3

# Connect to the database (creates it if it doesn't exist)
connection = sqlite3.connect("data/sensor_data.db")

cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_id TEXT,
    commodity TEXT,
    temperature REAL,
    humidity REAL,
    vibration REAL,
    market_price REAL,
    safe_temp REAL,
    max_humidity REAL,
    origin TEXT,
    destination TEXT,
    distance_remaining REAL,
    timestamp TEXT
)
""")