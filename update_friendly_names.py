import urllib.request
import json
import ssl
import sqlite3
import psycopg2
import os

db_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\sc_database.db"

# PostgreSQL connection configurations (fallback to load_dotenv logic)
def load_dotenv():
    env_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\.env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'\"")

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "guild_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "choose_a_strong_password")

endpoints = [
    "https://server.erkul.games/live/weapons",
    "https://server.erkul.games/live/shields",
    "https://server.erkul.games/live/coolers",
    "https://server.erkul.games/live/power-plants",
    "https://server.erkul.games/live/qdrives",
    "https://server.erkul.games/live/radars",
    "https://server.erkul.games/live/missiles",
    "https://server.erkul.games/live/missile-racks"
]

def fetch_erkul(url):
    headers = {
        "Origin": "https://www.erkul.games",
        "Referer": "https://www.erkul.games/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    mappings = {}
    
    print("Fetching friendly names mapping from Erkul API...")
    for url in endpoints:
        print(f"Fetching {url.split('/')[-1]}...")
        items = fetch_erkul(url)
        if not items:
            continue
            
        for item in items:
            local_name = item.get("localName")
            if not local_name:
                continue
                
            data_block = item.get("data", {})
            friendly_name = data_block.get("name")
            mfg_name = None
            item_class = data_block.get("class")
            
            mfg_data = data_block.get("manufacturerData", {}).get("data", {})
            if mfg_data:
                mfg_name = mfg_data.get("name")
                
            if friendly_name:
                # Store friendly name, manufacturer and classification for this class name
                mappings[local_name.lower()] = {
                    "name": friendly_name,
                    "manufacturer": mfg_name,
                    "classification": item_class
                }
                
    print(f"Loaded {len(mappings)} mappings from Erkul API.")
    
    # 1. Update SQLite
    if os.path.exists(db_path):
        print("Updating SQLite database...")
        sqlite_conn = sqlite3.connect(db_path)
        cursor = sqlite_conn.cursor()
        
        updated_count = 0
        for class_name_lower, info in mappings.items():
            cursor.execute("""
                UPDATE components 
                SET name = ?, manufacturer = COALESCE(?, manufacturer), classification = ? 
                WHERE LOWER(class_name) = ?;
            """, (info["name"], info["manufacturer"], info["classification"], class_name_lower))
            if cursor.rowcount > 0:
                updated_count += cursor.rowcount
                
        sqlite_conn.commit()
        sqlite_conn.close()
        print(f"Updated {updated_count} components in SQLite database with friendly names.")
    else:
        print("SQLite Database not found!")
        
    # 2. Update PostgreSQL
    print("Updating PostgreSQL database...")
    try:
        pg_conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        pg_cursor = pg_conn.cursor()
        
        pg_updated = 0
        for class_name_lower, info in mappings.items():
            pg_cursor.execute("""
                UPDATE components 
                SET name = %s, manufacturer = COALESCE(%s, manufacturer), classification = %s 
                WHERE LOWER(class_name) = %s;
            """, (info["name"], info["manufacturer"], info["classification"], class_name_lower))
            if pg_cursor.rowcount > 0:
                pg_updated += pg_cursor.rowcount
                
        pg_conn.commit()
        pg_conn.close()
        print(f"Updated {pg_updated} components in PostgreSQL database with friendly names.")
    except Exception as e:
        print("Error updating PostgreSQL:", e)

if __name__ == "__main__":
    main()
