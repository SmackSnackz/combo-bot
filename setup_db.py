import sqlite3
import os

if os.path.exists("combobot.db"):
    os.remove("combobot.db")


conn = sqlite3.connect("combobot.db")
cursor = conn.cursor()

with open("schema.sql", "r") as f:
    schema = f.read() 

cursor.executescript(schema)

with open ("seed.sql", "r") as f:
    seed = f.read()

cursor.executescript(seed)

conn.commit()

for table in ("people", "wallets", "orders"):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(table, cursor.fetchone()[0])

conn.close()
