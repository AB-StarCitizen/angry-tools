# Star Citizen Game Data Parsing & Database Sync - Summary

This document serves as a persistent record of the actions taken, discoveries made, and scripts developed for parsing the *Star Citizen* data-mined JSON files and syncing them to a database.

---

## 1. Remote API Research (Erkul.games)
We analyzed the client-side JavaScript of [Erkul.games](https://www.erkul.games/live/calculator) (specifically `main.5d3419f96e07cfdc.js`) to find their JSON data endpoints.

### Findings:
* **Base URL**: `https://server.erkul.games`
* **JSON Endpoints**:
  * Ships: `https://server.erkul.games/live/ships`
  * Shop Pricing & Locations: `https://server.erkul.games/shop`
  * Version Info: `https://server.erkul.games/informations`
  * Differences: `https://server.erkul.games/live-differences`
  * Component Categories: `/live/weapons`, `/live/shields`, `/live/coolers`, `/live/power-plants`, `/live/qdrives`, `/live/jumpdrives`, `/live/missiles`, `/live/missile-racks`, `/live/turrets`, `/live/paints`, `/live/qeds`, `/live/radars`, `/live/modules`, `/live/bombs`, `/live/utilities`, `/live/controllers`, `/live/mounts`.
* **Request Security (HTTP 418 Bypass)**:
  Direct scripting to the endpoints returns a `418 I'm a Teapot` error. The server requires headers to bypass this:
  ```http
  Origin: https://www.erkul.games
  Referer: https://www.erkul.games/
  User-Agent: [Standard Browser User-Agent]
  ```

---

## 2. Local File Structures (Foundry Records)
We analyzed the local directory `libs/foundry/records` containing the offline converted game files. These parsed JSON files are obtained and data-mined from the game's PKG files using [StarBreaker](https://github.com/diogotr7/StarBreaker):
* **Ships**: Stored in `entities/spaceships/*.json` (e.g. `anvl_arrow.json`).
* **Components**: Stored in subfolders of `entities/scitem/ships/` (e.g., `cooler/`, `powerplant/`, `quantumdrive/`, `shieldgenerator/`, `weapons/`, `missile_racks/`).
* **Shop data**: Stored in `globalshopparams/*.json`.

---

## 3. Database Development & Sync Scripts
We developed scripts to parse these local JSON records and import them into SQLite and PostgreSQL databases. The databases are configured to filter out AI/NPC templates and only contain player pledge ships (importing 193 unique spaceships and ground vehicles, along with their port layouts and components).

### Database Schema (PostgreSQL with UUIDs):
1. **`ships`**: Stores metadata for all ships and vehicles.
   * `id`: `UUID PRIMARY KEY DEFAULT uuid_generate_v4()`
   * `class_name`: `VARCHAR(255) UNIQUE` (e.g., `ANVL_Arrow`)
   * `display_name`, `description`, `career`, `role`, `manufacturer`
2. **`components`**: Stores all attachable ship items.
   * `id`: `UUID PRIMARY KEY DEFAULT uuid_generate_v4()`
   * `class_name`: `VARCHAR(255) UNIQUE`
   * `name`, `type` (e.g., `PowerPlant`), `sub_type`, `size`, `grade`, `manufacturer`
3. **`ship_ports`**: Maps ports, including nested slots (like weapons inside gimbals/turrets).
   * `id`: `UUID PRIMARY KEY DEFAULT uuid_generate_v4()`
   * `ship_id`: `UUID REFERENCES ships(id)`
   * `port_name`: `VARCHAR(255)`
   * `parent_port`: `VARCHAR(255) DEFAULT ''` (tracks slot nesting)
   * `min_size`, `max_size`, `accepted_types`, `default_component_class`
4. **`ship_default_loadouts`**: Maps ships to their equipped components (many-to-many junction table).
   * `id`: `UUID PRIMARY KEY DEFAULT uuid_generate_v4()`
   * `ship_id`: `UUID REFERENCES ships(id)`
   * `port_name`: `VARCHAR(255)`
   * `parent_port`: `VARCHAR(255) DEFAULT ''`
   * `component_id`: `UUID REFERENCES components(id)`
5. **`file_sync_metadata`**: Tracks file synchronization states.
   * `file_path`: `VARCHAR(512) PRIMARY KEY`
   * `last_modified`: `DOUBLE PRECISION`
   * `file_size`: `BIGINT`

---

## 4. Key Script Mechanisms (Implemented in `build_sc_db_pg.py`)

* **Incremental Sync / Modification Detection**:
  The script monitors file modification timestamps (`mtime`) and file sizes. If they match the entries in `file_sync_metadata`, the file is skipped.
* **Component Pre-Loading**:
  To allow fast skipping, existing component records are loaded from the database into memory at startup. This ensures the ship loadout parser can resolve sizes/types even when skipping unchanged component JSON files.
* **Ship Hardpoint Change Updates**:
  If a ship file is modified, the script re-runs. Before inserting the new layout, it runs a `DELETE FROM ship_ports WHERE ship_id = %s;` to remove old records. This prevents orphaned or outdated hardpoints from persisting in the database.
* **Recursive Loadout Traversal**:
  Traverses loadouts nested inside other attachments (such as gimbal mounts, turrets, and missile launchers) to capture sub-level weapons and items.
* **Pledge Ship Filtering**:
  Both build scripts scan the vehicle showroom display definitions in `entities/scitem/shopdisplays/vehicle/*.json` to extract allowed ship tags (`RequiredPortTags`), map display-specific variations (e.g. `AEGS_Retaliator_Base` to `AEGS_Retaliator`, `ANVL_Pisces` to `ANVL_C8_Pisces`), and filter spaceship and ground vehicle JSON files to skip non-pledge (AI-only, NPC templates, test, or template) ship entries during database synchronization.

---

## 5. Script Files Reference
The scripts and database files reside in the root workspace directory `C:\Users\mpsoa\Desktop\SC_4.8_data\`:
1. [build_sc_db.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db.py): Rebuilds the SQLite database [sc_database.db](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/sc_database.db) with the normalized schema and `ship_default_loadouts` table.
2. [build_sc_db_pg.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db_pg.py): PostgreSQL script featuring incremental updates, change detection, UUID primary keys, and the new loadouts table.
3. [update_friendly_names.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/update_friendly_names.py): Fetches real in-game names and manufacturer names from the Erkul API and maps them to components inside the SQLite and PostgreSQL databases.
4. [generate_loadouts_report.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/generate_loadouts_report.py): Compiles the Markdown loadouts catalog directly from the SQLite database.
5. [generate_pledge_report.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/generate_pledge_report.py): Compiles the pledge/ownable ships report from the SQLite database.
6. [export_loadouts_json.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/export_loadouts_json.py): Exports default ship loadouts to a structured JSON file.
7. [query_counts.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/query_counts.py): Helper script to query SQLite database row counts.
8. [query_pg_counts.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/query_pg_counts.py): Helper script to query PostgreSQL database row counts.

To run the database build/sync scripts from the root directory:
```bash
python build_sc_db.py
python build_sc_db_pg.py
python update_friendly_names.py
python generate_loadouts_report.py
python generate_pledge_report.py
python export_loadouts_json.py
```
*(PostgreSQL connection parameters are loaded from the [.env](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/.env) file).*

---

## 6. Generated Reports Reference
We compiled catalogs directly from the finalized database:
1. [pledge_ships_report.md](file:///C:/Users/mpsoa/.gemini/antigravity/brain/9d2aa908-24a9-4436-b2e5-56f2fea32cff/pledge_ships_report.md) (Brain Artifact): Grouped inventory of all 193 user-ownable spaceships, ground vehicles, and power suits.
2. [ship_default_loadouts.md](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/ship_default_loadouts.md) (Root Folder & Brain Artifact): Comprehensive markdown catalog of default equipped components.
3. [ship_default_loadouts.json](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/ship_default_loadouts.json) (Root Folder): Structured JSON file containing all default ship loadouts, grouped by component category under each ship.


