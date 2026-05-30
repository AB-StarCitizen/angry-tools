import sqlite3
import os

db_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\sc_database.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT count(*) FROM ships")
        print("Ships count in SQLite:", c.fetchone()[0])
        c.execute("SELECT count(*) FROM ship_ports")
        print("Ship ports count in SQLite:", c.fetchone()[0])
        c.execute("SELECT count(*) FROM components")
        print("Components count in SQLite:", c.fetchone()[0])
    except Exception as e:
        print("Error querying database:", e)
    finally:
        conn.close()
else:
    print("Database file does not exist!")
