import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

container_ids = ["C101", "C102", "C103", "C104", "C105"]

while True:
    sensor_data = {
        "container_id": random.choice(container_ids),
        "temperature": round(random.uniform(2.0, 10.0), 2),
        "humidity": round(random.uniform(60.0, 90.0), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    producer.send("container_sensor_data", sensor_data)
    print("Sent:", sensor_data)

    time.sleep(2)