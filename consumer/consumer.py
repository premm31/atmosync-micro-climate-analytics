from kafka import KafkaConsumer
import sqlite3
import json

# Connect to SQLite database
connection = sqlite3.connect("data/sensor_data.db")
cursor = connection.cursor()

# Create table if it doesn't exist
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

connection.commit()

# Connect to Kafka
consumer = KafkaConsumer(
    "container_sensor_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started... Waiting for data...\n")

for message in consumer:
    data = message.value

    print("Received:", data)

    cursor.execute("""
    INSERT INTO sensor_data (
        container_id,
        commodity,
        temperature,
        humidity,
        vibration,
        market_price,
        safe_temp,
        max_humidity,
        origin,
        destination,
        distance_remaining,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["container_id"],
        data["commodity"],
        data["temperature"],
        data["humidity"],
        data["vibration"],
        data["market_price"],
        data["safe_temp"],
        data["max_humidity"],
        data["origin"],
        data["destination"],
        data["distance_remaining"],
        data["timestamp"]
    ))

    connection.commit()