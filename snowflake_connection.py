import os
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
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

print("✅ Connected to Snowflake Successfully!")

cursor = conn.cursor()

cursor.execute("SELECT CURRENT_VERSION();")

print("Snowflake Version:", cursor.fetchone())

cursor.close()
conn.close()

print("✅ Connection Closed.")