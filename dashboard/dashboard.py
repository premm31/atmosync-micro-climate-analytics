import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌡️",
    layout="wide"
)

load_dotenv()

# Auto Refresh Every 5 Seconds
st_autorefresh(interval=5000, key="refresh")

# ---------------- SIDEBAR ----------------

st.sidebar.title("🌡️ AtmoSync")

st.sidebar.markdown("---")

st.sidebar.info("""
### Real-Time IoT Monitoring

Pipeline

IoT Sensors

⬇

Kafka

⬇

Snowflake

⬇

dbt

⬇

Dashboard
""")

st.sidebar.markdown("---")

st.sidebar.success("🟢 Pipeline Running")

# ---------------- TITLE ----------------

st.title("🌡️ AtmoSync - Real-Time IoT Monitoring Dashboard")

st.caption(
    f"Last Updated : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# ---------------- SNOWFLAKE CONNECTION ----------------

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

query = """
SELECT *
FROM SENSOR_DATA
ORDER BY TIMESTAMP DESC
LIMIT 100
"""

df = pd.read_sql(query, conn)

conn.close()

# ---------------- EMPTY CHECK ----------------

if df.empty:
    st.warning("No data available.")
    st.stop()

# Table (latest first)
table_df = df.reset_index(drop=True)

# Charts (oldest first)
df = df.iloc[::-1].reset_index(drop=True)

# ---------------- KPI ----------------

st.subheader("📊 Dashboard Summary")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "🌡 Avg Temperature",
    f"{df['TEMPERATURE'].mean():.2f} °C"
)

k2.metric(
    "💧 Avg Humidity",
    f"{df['HUMIDITY'].mean():.2f} %"
)

k3.metric(
    "📦 Containers",
    df["CONTAINER_ID"].nunique()
)

k4.metric(
    "📄 Records",
    len(df)
)

# ---------------- STATUS ----------------

s1, s2, s3 = st.columns(3)

s1.success("🟢 Kafka Running")
s2.success("🟢 Snowflake Connected")
s3.success("🟢 Dashboard Live")

# ---------------- FILTER ----------------

st.subheader("🔍 Filter")

container = st.selectbox(
    "Select Container",
    ["All"] + sorted(df["CONTAINER_ID"].unique().tolist())
)

if container != "All":
    df = df[df["CONTAINER_ID"] == container]

# ---------------- ALERTS ----------------

st.subheader("🚨 Alerts")

high_temp = df[df["TEMPERATURE"] > 10]

high_humidity = df[df["HUMIDITY"] > 85]

if high_temp.empty and high_humidity.empty:

    st.success("✅ All containers are operating within safe limits.")

else:

    if not high_temp.empty:
        st.error(
            f"🔥 {len(high_temp)} container(s) have High Temperature."
        )

    if not high_humidity.empty:
        st.warning(
            f"💧 {len(high_humidity)} container(s) have High Humidity."
        )

# ---------------- CHARTS ----------------

col1, col2 = st.columns(2)

with col1:

    fig = px.line(
        df,
        x="TIMESTAMP",
        y="TEMPERATURE",
        markers=True,
        title="Temperature Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.line(
        df,
        x="TIMESTAMP",
        y="HUMIDITY",
        markers=True,
        title="Humidity Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- VIBRATION ----------------

fig = px.bar(
    df,
    x="CONTAINER_ID",
    y="VIBRATION",
    color="CONTAINER_ID",
    title="Container Vibration"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- PIE ----------------

fig = px.pie(
    df,
    names="COMMODITY",
    title="Commodity Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- DISTANCE ----------------

fig = px.bar(
    df,
    x="CONTAINER_ID",
    y="DISTANCE_REMAINING",
    color="COMMODITY",
    title="Distance Remaining"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- TABLE ----------------

st.subheader("📋 Latest Sensor Data")

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=False
)
# ---------------- DOWNLOAD ----------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Latest Data",
    csv,
    "sensor_data.csv",
    "text/csv"
)

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
### 👨‍💻 Developed By

**Prem**

**B.Tech – Computer Science & Engineering (Data Science)**

**Project:** AtmoSync – Real-Time IoT Monitoring & Analytics

**Technologies Used**

- Python
- Apache Kafka
- Docker
- Snowflake
- dbt
- Streamlit
- Plotly
""")