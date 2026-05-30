import psycopg2
import os

# Manual fallback loader to read environment variables from .env if present without external dependencies
def load_dotenv():
    for base in [os.path.dirname(os.path.abspath(__file__)), os.getcwd()]:
        env_path = os.path.join(base, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip().strip("'\"")
            break

load_dotenv()

# PostgreSQL connection configurations
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "guild_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "choose_a_strong_password")

def query_pg():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ships;")
        ships_count = cursor.fetchone()[0]
        print(f"Ships count in PG: {ships_count}")
        
        cursor.execute("SELECT COUNT(*) FROM ship_ports;")
        ports_count = cursor.fetchone()[0]
        print(f"Ship ports count in PG: {ports_count}")
        
        cursor.execute("SELECT COUNT(*) FROM components;")
        components_count = cursor.fetchone()[0]
        print(f"Components count in PG: {components_count}")
        
        # Query new ship default loadouts table
        try:
            cursor.execute("SELECT COUNT(*) FROM ship_default_loadouts;")
            loadouts_count = cursor.fetchone()[0]
            print(f"Default loadout rows in PG: {loadouts_count}")
        except Exception as e:
            print("Could not query ship_default_loadouts count in PG:", e)
        
        # Verify that an AI variant ship is not in the DB
        cursor.execute("SELECT COUNT(*) FROM ships WHERE class_name = 'ANVL_Arrow_PU_AI_Crim';")
        ai_arrow_count = cursor.fetchone()[0]
        print(f"ANVL_Arrow_PU_AI_Crim count in PG: {ai_arrow_count}")
        
        # Verify that a player ship is in the DB
        cursor.execute("SELECT COUNT(*) FROM ships WHERE class_name = 'ANVL_Arrow';")
        player_arrow_count = cursor.fetchone()[0]
        print(f"ANVL_Arrow count in PG: {player_arrow_count}")
        
        conn.close()
    except Exception as e:
        print("Error connecting to or querying PG DB:", e)

if __name__ == "__main__":
    query_pg()
