import sqlite3

connection = sqlite3.connect("data/sensor_data.db")
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(sensor_data)")
columns = cursor.fetchall()

print("\nColumns in sensor_data table:\n")

for column in columns:
    print(column)