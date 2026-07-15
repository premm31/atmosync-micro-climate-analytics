# 🌡️ AtmoSync - Real-Time IoT Monitoring Dashboard

## 📌 Project Overview

AtmoSync is a real-time IoT monitoring system that simulates sensor data, streams it through Apache Kafka, stores it in an SQLite database, and visualizes the data using a Streamlit dashboard.

This project demonstrates how real-time data pipelines are built for applications such as cold chain monitoring, smart warehouses, logistics, and industrial IoT.

---

## 🚀 Technologies Used

- Python
- Apache Kafka
- ZooKeeper
- Docker
- SQLite
- Streamlit
- Plotly
- Pandas

---

## 📂 Project Architecture

```
IoT Sensor Simulator
        │
        ▼
Kafka Producer
        │
        ▼
Apache Kafka
        │
        ▼
Kafka Consumer
        │
        ▼
SQLite Database
        │
        ▼
Streamlit Dashboard
```

---

## 📁 Project Structure

```
AtmoSync/
│
├── producer/
├── consumer/
├── dashboard/
├── data/
├── docs/
├── dbt/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ✨ Features

- Real-time IoT sensor simulation
- Kafka-based message streaming
- SQLite database storage
- Live Streamlit dashboard
- Interactive Plotly charts
- Dockerized Kafka and ZooKeeper

---

## ▶️ How to Run

### 1. Start Docker containers

```bash
docker-compose up -d
```

### 2. Start the Producer

```bash
python producer/iot_simulator.py
```

### 3. Start the Consumer

```bash
python consumer/consumer.py
```

### 4. Launch the Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## 📊 Dashboard

The dashboard displays:

- Live sensor data
- Temperature graph
- Humidity graph
- Vibration graph

---

## 👨‍💻 Author

**Prem (premm31)**

Internship Project – AtmoSync