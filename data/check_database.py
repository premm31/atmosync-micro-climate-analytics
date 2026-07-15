import sqlite3

connection = sqlite3.connect("data/sensor_data.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM sensor_data")

rows = cursor.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("No data found in the table.")

connection.close()