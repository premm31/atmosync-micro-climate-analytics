import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AtmoSync Dashboard", layout="wide")

st.title("🌡️ AtmoSync - Real-Time IoT Dashboard")

connection = sqlite3.connect("data/sensor_data.db")

query = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 100"

df = pd.read_sql_query(query, connection)

connection.close()

if df.empty:
    st.warning("No data available.")
else:
    st.subheader("Latest Sensor Data")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        fig_temp = px.line(
            df.iloc[::-1],
            x="timestamp",
            y="temperature",
            title="Temperature"
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        fig_humidity = px.line(
            df.iloc[::-1],
            x="timestamp",
            y="humidity",
            title="Humidity"
        )
        st.plotly_chart(fig_humidity, use_container_width=True)

    fig_vibration = px.bar(
        df.iloc[::-1],
        x="container_id",
        y="vibration",
        color="container_id",
        title="Container Vibration"
    )

    st.plotly_chart(fig_vibration, use_container_width=True)