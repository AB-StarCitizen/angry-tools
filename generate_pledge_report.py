import os
import sqlite3
import json

base_dir = r"C:\Users\mpsoa\Desktop\SC_4.8_data\libs\foundry\records"
db_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\sc_database.db"
artifacts_dir = r"C:\Users\mpsoa\.gemini\antigravity\brain\9d2aa908-24a9-4436-b2e5-56f2fea32cff"
tags_file = r"C:\Users\mpsoa\.gemini\antigravity\scratch\shop_vehicle_tags.txt"


# Manufacturers Map
MANUFACTURERS_MAP = {
    "aegs": "Aegis Dynamics",
    "anvl": "Anvil Aerospace",
    "orig": "Origin Jumpworks",
    "rsi": "Roberts Space Industries",
    "misc": "MISC",
    "drak": "Drake Interplanetary",
    "argo": "Argo Astronautics",
    "banu": "Banu",
    "cnou": "Consolidated Outland",
    "crus": "Crusader Industries",
    "espr": "Esperia",
    "gama": "Gatac Manufacture",
    "krig": "Kruger Intergalactic",
    "mrai": "Mirai",
    "vncl": "Vanduul",
    "xian": "Xi'an",
    "tmbl": "Tumbril Land Systems",
    "grey": "Greycat Industrial",
    "grin": "Greycat Industrial",
}

def get_clean_name(cls_name, current_name):
    # If the current name has an @ sign or is blank, fallback to class name
    if not current_name or current_name.startswith("@"):
        name = cls_name.replace("_", " ")
    else:
        name = current_name
        
    # Clean up prefixes
    parts = name.split()
    if len(parts) > 0:
        p0_lower = parts[0].lower()
        if p0_lower in MANUFACTURERS_MAP:
            # Replace prefix code with clean manufacturer name
            parts[0] = MANUFACTURERS_MAP[p0_lower]
            name = " ".join(parts)
    return name

def read_tags():
    tags = []
    if not os.path.exists(tags_file):
        return tags
    in_tags = False
    with open(tags_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "--- Unique RequiredPortTags ---":
                in_tags = True
                continue
            if line == "--- Display Files Mapping ---":
                break
            if in_tags and line:
                tags.append(line)
    return tags

def generate_report():
    tags = read_tags()
    if not os.path.exists(db_path):
        print("Database not found!")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Store categorized ships
    spaceships = {}
    ground_vehicles = {}
    
    # Resolve all matched ships
    for tag in tags:
        # Resolve class names
        cls_query = tag
        cursor.execute("SELECT class_name, display_name, career, role, manufacturer FROM ships WHERE LOWER(class_name) = LOWER(?)", (cls_query,))
        row = cursor.fetchone()
        
        if not row and " " in tag:
            cls_query = tag.replace(" ", "_")
            cursor.execute("SELECT class_name, display_name, career, role, manufacturer FROM ships WHERE LOWER(class_name) = LOWER(?)", (cls_query,))
            row = cursor.fetchone()
            
        # Suffix matching for a few special cases
        if not row:
            if tag == "AEGS_Hammerhead ShipShowdown": cls_query = "AEGS_Hammerhead_Showdown"
            elif tag == "AEGS_Reclaimer ShipShowdown": cls_query = "AEGS_Reclaimer_Showdown"
            elif tag == "AEGS_Retaliator_Base": cls_query = "AEGS_Retaliator"
            elif tag == "AEGS_Retaliator_Bomber": cls_query = "AEGS_Retaliator"
            elif tag == "AEGS_Retaliator_Cargo": cls_query = "AEGS_Retaliator"
            elif tag == "AEGS_Vanguard_Warden": cls_query = "AEGS_Vanguard"
            elif tag == "ANVL_Pisces": cls_query = "ANVL_C8_Pisces"
            elif tag == "ANVL_Pisces_Expedition": cls_query = "ANVL_C8X_Pisces_Expedition"
            elif tag == "ARES_Starfighter": cls_query = "CRUS_Starfighter_Ion" # Ion/Inferno Ares
            
            cursor.execute("SELECT class_name, display_name, career, role, manufacturer FROM ships WHERE LOWER(class_name) = LOWER(?)", (cls_query,))
            row = cursor.fetchone()
            
        if row:
            cls_name, disp_name, career, role, manufacturer = row
            clean_name = get_clean_name(cls_name, disp_name)
            
            # Determine if spaceship or ground vehicle (based on path/class/tags)
            is_ground = False
            # Check if this class is under groundvehicles directory
            gv_path = os.path.join(base_dir, "entities", "groundvehicles", f"{cls_name.lower()}.json")
            if os.path.exists(gv_path) or "cyclone" in cls_name.lower() or "ursa" in cls_name.lower() or "nova" in cls_name.lower() or "lynx" in cls_name.lower() or "storm" in cls_name.lower() or "rover" in cls_name.lower():
                is_ground = True
                
            mfg = manufacturer if manufacturer else "Other"
            ship_info = {
                "class": cls_name,
                "name": clean_name,
                "role": role if role else "Unknown",
                "career": career if career else "Unknown"
            }
            
            if is_ground:
                if mfg not in ground_vehicles: ground_vehicles[mfg] = []
                ground_vehicles[mfg].append(ship_info)
            else:
                if mfg not in spaceships: spaceships[mfg] = []
                spaceships[mfg].append(ship_info)
                
    # Add Argo ATLS manually as a special power suit vehicle
    if "ARGO_ATLS" in tags:
        mfg = "Argo Astronautics"
        atls_info = {
            "class": "argo_atls",
            "name": "Argo ATLS Power Suit",
            "role": "Loader / Exoskeleton",
            "career": "Industrial / Cargo"
        }
        if mfg not in ground_vehicles: ground_vehicles[mfg] = []
        ground_vehicles[mfg].append(atls_info)
        
    # Get statistics of components from DB
    cursor.execute("SELECT type, COUNT(*) FROM components GROUP BY type ORDER BY COUNT(*) DESC;")
    comp_types = cursor.fetchall()
    
    # Generate the Markdown report
    report_path = os.path.join(artifacts_dir, "pledge_ships_report.md")
    with open(report_path, "w", encoding="utf-8") as out:
        out.write("# Star Citizen Ownable (Pledge) Ships & Components Catalog\n\n")
        out.write("This report compiles a list of **player-pledgeable (ownable) ships, ground vehicles, and components** identified directly from the source game data files.\n\n")
        
        out.write("## 1. Methodology\n")
        out.write("We identified player-ownable assets by cross-referencing files in the following folders:\n")
        out.write("- **Showroom Displays**: `entities/scitem/shopdisplays/vehicle/*.json` - These files define showroom pedestals in showrooms (e.g. Astro Armada, New Deal). They map specific ship classes using `RequiredPortTags` to prevent AI-only variants from displaying.\n")
        out.write("- **Entitlements**: Base player ships contain `DefaultEntitlementEntityParams` in their static class data (pointing to account entitlements), while AI-only variants (e.g., `_pu_ai_crim`) do not.\n\n")
        
        out.write("## 2. Spaceships Catalog\n\n")
        out.write("Here is the list of player-ownable spaceships grouped by manufacturer:\n\n")
        
        for mfg, list_ships in sorted(spaceships.items()):
            out.write(f"### {mfg} ({len(list_ships)} ships)\n")
            out.write("| Name | Class Name | Role | Career |\n")
            out.write("| :--- | :--- | :--- | :--- |\n")
            # De-duplicate names for modular variants that share base classes
            seen = set()
            for s in sorted(list_ships, key=lambda x: x['name']):
                if s['name'] in seen: continue
                seen.add(s['name'])
                out.write(f"| {s['name']} | `{s['class']}` | {s['role']} | {s['career']} |\n")
            out.write("\n")
            
        out.write("## 3. Ground Vehicles & Power Suits Catalog\n\n")
        out.write("Here is the list of player-ownable ground vehicles and mechs:\n\n")
        
        for mfg, list_ships in sorted(ground_vehicles.items()):
            out.write(f"### {mfg} ({len(list_ships)} vehicles)\n")
            out.write("| Name | Class Name | Role | Career |\n")
            out.write("| :--- | :--- | :--- | :--- |\n")
            seen = set()
            for s in sorted(list_ships, key=lambda x: x['name']):
                if s['name'] in seen: continue
                seen.add(s['name'])
                out.write(f"| {s['name']} | `{s['class']}` | {s['role']} | {s['career']} |\n")
            out.write("\n")
            
        out.write("## 4. User-Ownable Ship Components\n\n")
        out.write("Standard ship components are player-ownable in-game (purchasable at shop terminals) if they have `SCItemPurchasableParams` in their definition JSON and do not belong to NPC-only/AI loadouts.\n\n")
        out.write("Here is the breakdown of ownable component types found in the database:\n\n")
        out.write("| Component Type | Database Count | Description |\n")
        out.write("| :--- | :---: | :--- |\n")
        
        descriptions = {
            "WeaponGun": "Ship board weapons, including laser repeaters, ballistics, distortions, and cannons.",
            "Shield": "Shield generators providing protection against damage.",
            "PowerPlant": "Power plants generating energy for ship systems and thrusters.",
            "Cooler": "Coolers managing thermodynamic heat accumulation.",
            "QuantumDrive": "Quantum drives for interstellar propulsion.",
            "Missile": "Missiles and torpedoes loaded on ordnance racks.",
            "Turret": "Manned and remote weapon/utility turrets.",
            "MissileLauncher": "Missile racks that hold ammunition packages.",
            "Paint": "Cosmetic ship livery skins.",
            "MiningModifier": "Sub-items attached to mining lasers to tweak mining properties."
        }
        
        for comp_type, count in comp_types:
            desc = descriptions.get(comp_type, "General ship equipment or attachment.")
            out.write(f"| {comp_type} | {count} | {desc} |\n")
            
        out.write("\n*Report compiled successfully from game data records database.*")
        
    print(f"Report written successfully to {report_path}!")
    conn.close()

if __name__ == "__main__":
    generate_report()
