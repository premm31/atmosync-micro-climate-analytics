import json
import random
import time
from datetime import datetime

import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

commodities = pd.read_csv("datasets/commodity_prices.csv")

cities = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune"
]

while True:

    item = commodities.sample().iloc[0]

    sensor_data = {

        "container_id": f"C{random.randint(100,120)}",

        "commodity": item["commodity"],

        "temperature": round(random.uniform(2,15),2),

        "humidity": round(random.uniform(60,95),2),

        "vibration": round(random.uniform(0.1,2.5),2),

        "market_price": int(item["market_price"]),

        "safe_temp": int(item["safe_temp"]),

        "max_humidity": int(item["max_humidity"]),

        "origin": random.choice(cities),

        "destination": random.choice(cities),

        "distance_remaining": random.randint(50,1200),

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.send("container_sensor_data", sensor_data)

    print(sensor_data)

    time.sleep(2)