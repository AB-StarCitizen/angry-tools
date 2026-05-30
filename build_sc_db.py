import os
import json
import sqlite3
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "sc_database.db")
base_dir = os.path.join(script_dir, "libs", "foundry", "records")

# Helper to map raw manufacturer codes to clean names
MANUFACTURERS_MAP = {
    "aegs": "Aegis Dynamics", "anvl": "Anvil Aerospace", "orig": "Origin Jumpworks",
    "rsi": "Roberts Space Industries", "misc": "MISC", "drak": "Drake Interplanetary",
    "argo": "Argo Astronautics", "banu": "Banu", "cnou": "Consolidated Outland",
    "crus": "Crusader Industries", "espr": "Esperia", "gama": "Gatac Manufacture",
    "krig": "Kruger Intergalactic", "mrai": "Mirai", "vncl": "Vanduul", "xian": "Xi'an",
    "tmbl": "Tumbril Land Systems", "grey": "Greycat Industrial", "grin": "Greycat Industrial",
    "amrs": "Apocalypse Arms", "behr": "Behring", "gats": "Gallenson Tactical Systems",
    "jokr": "Joker Shipyards", "kbar": "Klaus & Werner", "klwe": "Klaus & Werner",
    "kron": "Kronus", "mxox": "MaxOx", "tars": "Tarsus",
}

def clean_tag(tag):
    if not tag: return ""
    tag = re.sub(r"^@(item_Name|vehicle_Name|vehicle_focus|vehicle_class|item_Desc|vehicle_Desc)", "", tag)
    return tag.replace("_", " ").strip()

def get_fallback_name(class_name, attach_type):
    parts = class_name.split('_')
    mfg, model = "", ""
    if len(parts) >= 2:
        mfg = MANUFACTURERS_MAP.get(parts[1].lower(), parts[1].title())
    if len(parts) >= 4:
        model = parts[3].title()
    elif len(parts) >= 3:
        model = parts[2].title()
    else:
        model = class_name.title()
    type_str = attach_type if attach_type else "Component"
    type_str = re.sub(r'(?<!^)(?=[A-Z])', ' ', type_str)
    return f"{mfg} {model} {type_str}".strip()

def get_pledge_classes(base_dir):
    display_dir = os.path.join(base_dir, "entities", "scitem", "shopdisplays", "vehicle")
    pledge_classes = set()
    if not os.path.exists(display_dir):
        return pledge_classes
        
    for file in os.listdir(display_dir):
        if file.endswith('.json'):
            path = os.path.join(display_dir, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                val = data.get("_RecordValue_", {})
                for comp in val.get("Components", []):
                    if comp.get("_Type_") == "SItemPortContainerComponentParams":
                        for port in comp.get("Ports", []):
                            p_tags = port.get("RequiredPortTags", "")
                            if p_tags:
                                for t in p_tags.split(','):
                                    t = t.strip().replace(" ", "_").lower()
                                    if t:
                                        pledge_classes.add(t)
            except Exception:
                pass
                
    # Apply manual mappings for display tags that point to different database class names
    mappings = {
        "aegs_hammerhead_shipshowdown": ["aegs_hammerhead_showdown"],
        "aegs_reclaimer_shipshowdown": ["aegs_reclaimer_showdown"],
        "aegs_retaliator_base": ["aegs_retaliator"],
        "aegs_retaliator_bomber": ["aegs_retaliator"],
        "aegs_retaliator_cargo": ["aegs_retaliator"],
        "aegs_vanguard_warden": ["aegs_vanguard"],
        "anvl_pisces": ["anvl_c8_pisces"],
        "anvl_pisces_expedition": ["anvl_c8x_pisces_expedition"],
        "ares_starfighter": ["crus_starfighter_ion", "crus_starfighter_inferno"],
    }
    
    extra_classes = []
    for tag, db_classes in mappings.items():
        if tag in pledge_classes:
            extra_classes.extend(db_classes)
            
    for cls in extra_classes:
        pledge_classes.add(cls.lower())
        
    return pledge_classes


def setup_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT UNIQUE NOT NULL,
        display_name TEXT,
        description TEXT,
        career TEXT,
        role TEXT,
        manufacturer TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT UNIQUE NOT NULL,
        name TEXT,
        type TEXT,
        sub_type TEXT,
        size INTEGER,
        grade TEXT,
        manufacturer TEXT,
        classification TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ship_ports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER NOT NULL,
        port_name TEXT NOT NULL,
        parent_port TEXT,
        min_size INTEGER,
        max_size INTEGER,
        accepted_types TEXT,
        default_component_class TEXT,
        FOREIGN KEY (ship_id) REFERENCES ships(id) ON DELETE CASCADE,
        UNIQUE(ship_id, port_name, parent_port)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ship_default_loadouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER NOT NULL,
        port_name TEXT NOT NULL,
        parent_port TEXT,
        component_id INTEGER NOT NULL,
        FOREIGN KEY (ship_id) REFERENCES ships(id) ON DELETE CASCADE,
        FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
        UNIQUE(ship_id, port_name, parent_port)
    );
    """)
    conn.commit()

def parse_components(conn):
    cursor = conn.cursor()
    scitem_dir = os.path.join(base_dir, "entities", "scitem")
    components_db = {}
    target_dirs = [os.path.join(scitem_dir, "ships"), os.path.join(scitem_dir, "weapons")]
    
    for t_dir in target_dirs:
        if not os.path.exists(t_dir): continue
        for root, dirs, files in os.walk(t_dir):
            for file_name in files:
                if not file_name.endswith('.json'): continue
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                    record_name = data.get("_RecordName_", "")
                    if not record_name.startswith("EntityClassDefinition."): continue
                    class_name = record_name.split(".", 1)[1]
                    val = data.get("_RecordValue_", {})
                    for comp in val.get("Components", []):
                        if comp.get("_Type_") == "SAttachableComponentParams":
                            attach_def = comp.get("AttachDef", {})
                            c_type = attach_def.get("Type")
                            ALLOWED_TYPES = {"powerplant", "shield", "quantumdrive", "cooler", "radar", "weapongun", "missile", "missilelauncher"}
                            if not c_type or c_type.lower() not in ALLOWED_TYPES:
                                continue
                            c_subtype = attach_def.get("SubType")
                            c_size = attach_def.get("Size")
                            c_grade = attach_def.get("Grade")
                            if c_grade is not None:
                                grade_map = {1: "A", 2: "B", 3: "C", 4: "D"}
                                try:
                                    c_grade = grade_map.get(int(c_grade), str(c_grade))
                                except (ValueError, TypeError):
                                    c_grade = str(c_grade)
                            
                            mfg_ref = attach_def.get("Manufacturer")
                            mfg_name = ""
                            if mfg_ref:
                                mfg_code = os.path.basename(mfg_ref).replace("scitemmanufacturer.", "").replace(".json", "").lower()
                                mfg_name = MANUFACTURERS_MAP.get(mfg_code, mfg_code.upper())
                            else:
                                parts = class_name.split('_')
                                if len(parts) >= 2: mfg_name = MANUFACTURERS_MAP.get(parts[1].lower(), parts[1].title())
                                
                            clean_name = clean_tag(attach_def.get("Localization", {}).get("Name"))
                            if not clean_name: clean_name = get_fallback_name(class_name, c_type)
                            if "loc_placeholder" in clean_name.lower().replace(" ", "_"):
                                continue
                            
                            components_db[class_name.lower()] = {
                                "class_name": class_name, "name": clean_name, "type": c_type,
                                "sub_type": c_subtype, "size": c_size, "grade": c_grade, "manufacturer": mfg_name
                            }
                            cursor.execute("""
                            INSERT OR REPLACE INTO components (class_name, name, type, sub_type, size, grade, manufacturer)
                            VALUES (?, ?, ?, ?, ?, ?, ?);
                            """, (class_name, clean_name, c_type, c_subtype, c_size, c_grade, mfg_name))
                            break
                except Exception: pass
    conn.commit()
    return components_db

def parse_loadout_entries(entries, components_db, parent_port=None):
    ports = []
    if not entries: return ports
    for entry in entries:
        port_name = entry.get("itemPortName")
        if not port_name: continue
        equipped_class = entry.get("entityClassName", "")
        equipped_ref = entry.get("entityClassReference")
        if not equipped_class and equipped_ref:
            equipped_class = os.path.basename(equipped_ref).replace(".json", "")
        comp_info = components_db.get(equipped_class.lower())
        ports.append({
            "port_name": port_name, "parent_port": parent_port,
            "equipped_class": equipped_class if equipped_class else None, "comp_info": comp_info
        })
        sub_loadout = entry.get("loadout")
        if sub_loadout and isinstance(sub_loadout, dict):
            sub_entries = sub_loadout.get("entries", [])
            ports.extend(parse_loadout_entries(sub_entries, components_db, parent_port=port_name))
    return ports

def parse_ships(conn, components_db):
    cursor = conn.cursor()
    pledge_classes = get_pledge_classes(base_dir)
    print(f"Skipping non-pledge ships (Allowed: {len(pledge_classes)} classes)...")
    entities_dir = os.path.join(base_dir, "entities")
    ship_dirs = [os.path.join(entities_dir, "spaceships"), os.path.join(entities_dir, "groundvehicles")]
    
    for s_dir in ship_dirs:
        if not os.path.exists(s_dir): continue
        for file_name in os.listdir(s_dir):
            if not file_name.endswith('.json'): continue
            file_path = os.path.join(s_dir, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)
                record_name = data.get("_RecordName_", "")
                if not record_name.startswith("EntityClassDefinition."): continue
                class_name = record_name.split(".", 1)[1]
                
                if class_name.lower() not in pledge_classes:
                    continue
                    
                val = data.get("_RecordValue_", {})
                vehicle_params, loadout_params, ports_def = None, None, {}
                
                for comp in val.get("Components", []):
                    c_type = comp.get("_Type_")
                    if c_type == "VehicleComponentParams": vehicle_params = comp
                    elif c_type == "SEntityComponentDefaultLoadoutParams": loadout_params = comp
                    elif c_type == "SItemPortContainerComponentParams":
                        for port in comp.get("Ports", []):
                            p_name = port.get("Name")
                            if p_name:
                                p_types = [pt.get("Type") for pt in port.get("Types", [])]
                                ports_def[p_name] = (port.get("MinSize"), port.get("MaxSize"), p_types)
                                
                if not vehicle_params: continue
                display_name = clean_tag(vehicle_params.get("vehicleName"))
                if not display_name: display_name = class_name.replace("_", " ").title()
                desc = clean_tag(vehicle_params.get("vehicleDescription"))
                career = clean_tag(vehicle_params.get("vehicleCareer"))
                role = clean_tag(vehicle_params.get("vehicleRole"))
                mfg_ref = vehicle_params.get("manufacturer")
                mfg_name = ""
                if mfg_ref:
                    mfg_code = os.path.basename(mfg_ref).replace("scitemmanufacturer.", "").replace(".json", "").lower()
                    mfg_name = MANUFACTURERS_MAP.get(mfg_code, mfg_code.upper())
                else:
                    parts = class_name.split('_')
                    if len(parts) >= 2: mfg_name = MANUFACTURERS_MAP.get(parts[1].lower(), parts[1].title())
                
                cursor.execute("""
                INSERT OR REPLACE INTO ships (class_name, display_name, description, career, role, manufacturer)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (class_name, display_name, desc, career, role, mfg_name))
                ship_id = cursor.lastrowid
                
                loadout_ports = []
                if loadout_params:
                    entries = loadout_params.get("loadout", {}).get("entries", [])
                    loadout_ports = parse_loadout_entries(entries, components_db)
                
                ports_to_insert = {}
                for lp in loadout_ports:
                    port_name = lp["port_name"]
                    parent_port = lp["parent_port"]
                    eq_class = lp["equipped_class"]
                    comp_info = lp["comp_info"]
                    key = (port_name, parent_port)
                    
                    min_sz, max_sz, accepted_t = None, None, None
                    if port_name in ports_def:
                        min_sz, max_sz, p_types = ports_def[port_name]
                        accepted_t = ",".join(p_types) if p_types else None
                    if comp_info:
                        if min_sz is None: min_sz = comp_info["size"]
                        if max_sz is None: max_sz = comp_info["size"]
                        if not accepted_t: accepted_t = comp_info["type"]
                    if not accepted_t:
                        if "cooler" in port_name.lower(): accepted_t = "Cooler"
                        elif "shield" in port_name.lower(): accepted_t = "Shield"
                        elif "power" in port_name.lower(): accepted_t = "PowerPlant"
                        elif "quantum" in port_name.lower(): accepted_t = "QuantumDrive"
                        elif "weapon" in port_name.lower(): accepted_t = "WeaponGun"
                        
                    ports_to_insert[key] = {
                        "port_name": port_name, "parent_port": parent_port,
                        "min_size": min_sz, "max_size": max_sz,
                        "accepted_types": accepted_t, "default_component_class": eq_class
                    }
                for p_name, (min_sz, max_sz, p_types) in ports_def.items():
                    key = (p_name, None)
                    if key not in ports_to_insert:
                        ports_to_insert[key] = {
                            "port_name": p_name, "parent_port": None, "min_size": min_sz, "max_size": max_sz,
                            "accepted_types": ",".join(p_types) if p_types else None, "default_component_class": None
                        }
                ALLOWED_TYPES = {"powerplant", "shield", "quantumdrive", "cooler", "radar", "weapongun", "missile", "missilelauncher"}
                for key, pi in ports_to_insert.items():
                    is_allowed = False
                    if pi["accepted_types"]:
                        for t in pi["accepted_types"].split(","):
                            if t.strip().lower() in ALLOWED_TYPES:
                                is_allowed = True
                                break
                    if not is_allowed and pi["default_component_class"]:
                        cursor.execute("SELECT 1 FROM components WHERE LOWER(class_name) = LOWER(?);", (pi["default_component_class"],))
                        if cursor.fetchone():
                            is_allowed = True
                    if not is_allowed:
                        continue
                        
                    cursor.execute("""
                    INSERT OR IGNORE INTO ship_ports (ship_id, port_name, parent_port, min_size, max_size, accepted_types, default_component_class)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """, (ship_id, pi["port_name"], pi["parent_port"], pi["min_size"], pi["max_size"], pi["accepted_types"], pi["default_component_class"]))
                    
                    if pi["default_component_class"]:
                        cursor.execute("SELECT id FROM components WHERE LOWER(class_name) = LOWER(?);", (pi["default_component_class"],))
                        comp_row = cursor.fetchone()
                        if comp_row:
                            comp_id = comp_row[0]
                            cursor.execute("""
                            INSERT OR REPLACE INTO ship_default_loadouts (ship_id, port_name, parent_port, component_id)
                            VALUES (?, ?, ?, ?);
                            """, (ship_id, pi["port_name"], pi["parent_port"], comp_id))
            except Exception: pass
    conn.commit()

def main():
    if os.path.exists(db_path): os.remove(db_path)
    conn = sqlite3.connect(db_path)
    try:
        setup_db(conn)
        components_db = parse_components(conn)
        parse_ships(conn, components_db)
    finally: conn.close()

if __name__ == "__main__": main()
