import sqlite3
import os

db_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\sc_database.db"
artifacts_dir = r"C:\Users\mpsoa\.gemini\antigravity\brain\9d2aa908-24a9-4436-b2e5-56f2fea32cff"

def clean_tag(name):
    if not name: return ""
    return name.replace("_", " ").strip()

def generate_loadouts_report():
    if not os.path.exists(db_path):
        print("Database not found!")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Fetch all ships (pledge ships only in our DB now)
    cursor.execute("SELECT id, class_name, display_name, manufacturer, role FROM ships ORDER BY manufacturer, display_name;")
    ships = cursor.fetchall()
    print(f"Loaded {len(ships)} ships from database.")
    
    report_path = r"C:\Users\mpsoa\Desktop\SC_4.8_data\ship_default_loadouts.md"
    report_path_brain = os.path.join(artifacts_dir, "ship_default_loadouts.md")
    
    with open(report_path, "w", encoding="utf-8") as out:
        out.write("# Star Citizen Ship Default Loadouts Catalog\n\n")
        out.write("This document lists the default equipped components and weapons for each player-ownable ship, extracted from the game data records database.\n\n")
        out.write("## Table of Contents\n")
        
        # Build TOC grouped by manufacturer
        current_mfg = None
        for ship_id, class_name, display_name, manufacturer, role in ships:
            mfg = manufacturer if manufacturer else "Unknown Manufacturer"
            if mfg != current_mfg:
                current_mfg = mfg
                mfg_anchor = mfg.lower().replace(" ", "-").replace("&", "").replace("'", "")
                out.write(f"- [{mfg}](#{mfg_anchor})\n")
        out.write("\n---\n\n")
        
        current_mfg = None
        for ship_id, class_name, display_name, manufacturer, role in ships:
            mfg = manufacturer if manufacturer else "Unknown Manufacturer"
            if mfg != current_mfg:
                current_mfg = mfg
                out.write(f"## {mfg}\n\n")
                
            out.write(f"### {display_name} (`{class_name}`)\n")
            out.write(f"* **Role**: {role if role else 'Unknown'}\n\n")
            
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
            
            if not ports:
                out.write("*No default components or weapons listed in database for this ship template.*\n\n")
                continue
                
            # Categorize items
            categories = {}
            for row in ports:
                p_name = row[0]
                p_parent = row[1]
                p_min = row[2]
                p_max = row[3]
                p_types = row[4]
                c_class = row[5]
                c_name = row[6]
                c_type = row[7]
                c_subtype = row[8]
                c_size = row[9]
                c_grade = row[10]
                c_mfg = row[11]
                c_classification = row[12]
                
                # Clean up type name for categorization
                cat = c_type if c_type else "Other Attachments"
                
                ALLOWED_TYPES = {"powerplant", "shield", "quantumdrive", "cooler", "radar", "weapongun", "missile", "missilelauncher"}
                if not cat or cat.lower() not in ALLOWED_TYPES:
                    continue
                    
                if cat not in categories:
                    categories[cat] = []
                    
                categories[cat].append({
                    "port": p_name,
                    "parent": p_parent,
                    "comp_name": c_name,
                    "comp_class": c_class,
                    "size": c_size,
                    "grade": c_grade,
                    "mfg": c_mfg,
                    "classification": c_classification
                })
                
            # Print categories
            for cat, items in sorted(categories.items()):
                # Format category name nicely
                cat_display = cat
                if cat == "Shield": cat_display = "Shield Generators"
                elif cat == "PowerPlant": cat_display = "Power Plants"
                elif cat == "Cooler": cat_display = "Coolers"
                elif cat == "QuantumDrive": cat_display = "Quantum Drives"
                elif cat == "WeaponGun": cat_display = "Weapons (Guns / Lasers)"
                elif cat == "Missile": cat_display = "Missiles / Torpedoes"
                elif cat == "MissileLauncher": cat_display = "Missile Racks"
                elif cat == "Turret": cat_display = "Turrets / Mounts"
                elif cat == "Paint": cat_display = "Default Paints"
                
                out.write(f"#### {cat_display}\n")
                out.write("| Port Name | Parent Port | Component Name | Size | Grade | Classification | Manufacturer | Class Name |\n")
                out.write("| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |\n")
                for item in sorted(items, key=lambda x: x['port']):
                    parent_display = item['parent'] if item['parent'] else "-"
                    grade_display = item['grade'] if item['grade'] else "-"
                    class_display = item['classification'] if item['classification'] else "-"
                    out.write(f"| {item['port']} | {parent_display} | {item['comp_name']} | S{item['size']} | {grade_display} | {class_display} | {item['mfg']} | `{item['comp_class']}` |\n")
                out.write("\n")
            out.write("---\n\n")
            
    import shutil
    shutil.copy2(report_path, report_path_brain)
    print(f"Report successfully written to {report_path} and copied to brain artifacts!")
    conn.close()

if __name__ == "__main__":
    generate_loadouts_report()
