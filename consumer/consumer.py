from kafka import KafkaConsumer
import json
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cursor = conn.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "container_sensor_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Consumer started... Waiting for data...\n")

for message in consumer:
    data = message.value

    print("Received:", data)

    cursor.execute("""
        INSERT INTO SENSOR_DATA
        (
            CONTAINER_ID,
            COMMODITY,
            TEMPERATURE,
            HUMIDITY,
            VIBRATION,
            MARKET_PRICE,
            SAFE_TEMP,
            MAX_HUMIDITY,
            ORIGIN,
            DESTINATION,
            DISTANCE_REMAINING,
            TIMESTAMP
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

    conn.commit()