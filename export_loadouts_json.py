import sqlite3
import os
import json

db_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\sc_database.db"
output_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\ship_default_loadouts.json"

def export_loadouts_to_json():
    if not os.path.exists(db_path):
        print("Database not found!")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all ships
    cursor.execute("SELECT id, class_name, display_name, manufacturer, role, career, description FROM ships ORDER BY manufacturer, display_name;")
    ships = cursor.fetchall()
    
    loadouts_catalog = []
    
    for ship_id, class_name, display_name, manufacturer, role, career, description in ships:
        # Fetch default components for this ship
        cursor.execute("""
            SELECT p.port_name, p.parent_port, p.min_size, p.max_size, p.accepted_types, 
                   c.class_name, c.name, c.type, c.sub_type, c.size, c.grade, c.manufacturer, c.classification
            FROM ship_ports p
            JOIN components c ON LOWER(p.default_component_class) = LOWER(c.class_name)
            WHERE p.ship_id = ? AND p.default_component_class IS NOT NULL AND p.default_component_class != ''
            ORDER BY c.type, p.port_name;
        """, (ship_id,))
        ports = cursor.fetchall()
        
        ALLOWED_TYPES = {"powerplant", "shield", "quantumdrive", "cooler", "radar", "weapongun", "missile", "missilelauncher"}
        
        loadout_by_category = {}
        for row in ports:
            p_name, p_parent, p_min, p_max, p_types, c_class, c_name, c_type, c_subtype, c_size, c_grade, c_mfg, c_classification = row
            
            if not c_type or c_type.lower() not in ALLOWED_TYPES:
                continue
                
            cat = c_type
            if cat not in loadout_by_category:
                loadout_by_category[cat] = []
                
            loadout_by_category[cat].append({
                "port_name": p_name,
                "parent_port": p_parent if p_parent else None,
                "component_class": c_class,
                "component_name": c_name,
                "size": c_size,
                "grade": c_grade if c_grade else None,
                "classification": c_classification if c_classification else None,
                "manufacturer": c_mfg if c_mfg else None,
                "sub_type": c_subtype if c_subtype else None,
                "min_port_size": p_min,
                "max_port_size": p_max,
                "accepted_types": p_types.split(",") if p_types else []
            })
            
        loadouts_catalog.append({
            "class_name": class_name,
            "display_name": display_name,
            "manufacturer": manufacturer if manufacturer else None,
            "role": role if role else None,
            "career": career if career else None,
            "description": description if description else None,
            "default_loadout": loadout_by_category
        })
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(loadouts_catalog, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully exported {len(loadouts_catalog)} ship loadouts to {output_path}")
    conn.close()

if __name__ == "__main__":
    export_loadouts_to_json()
