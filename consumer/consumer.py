from kafka import KafkaConsumer
import sqlite3
import json

# Connect to SQLite database
connection = sqlite3.connect("data/sensor_data.db")
cursor = connection.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "container_sensor_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started... Waiting for data.\n")

for message in consumer:
    data = message.value

    print("Received:", data)

    cursor.execute("""
    INSERT INTO sensor_data
    (container_id, temperature, humidity, vibration, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["container_id"],
        data["temperature"],
        data["humidity"],
        data["vibration"],
        data["timestamp"]
    ))

    connection.commit()