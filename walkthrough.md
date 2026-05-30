# Walkthrough - Component Classification, Grade Mapping & Placeholder Clean-up

We have adjusted both database builders, updated the friendly names script, and regenerated all reports to include item classifications, mapped letter grades, and filter out all components containing `@LOC PLACEHOLDER` in their localization name.

## Summary of Work Accomplished

1. **Database Schema & Builder Updates**:
   - Added `classification` column to the `components` table in [build_sc_db.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db.py) and [build_sc_db_pg.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db_pg.py).
   - Ensured `grade` uses `TEXT`/`VARCHAR(255)` with 1-4 mapped to A-D letters.
   - Updated component parsing in both builders to skip any component where the name contains `@LOC PLACEHOLDER` or `@LOC_PLACEHOLDER` (case-insensitive check: `"loc_placeholder" in clean_name.lower().replace(" ", "_")`).

2. **Integration with Erkul API**:
   - Modified [update_friendly_names.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/update_friendly_names.py) to fetch and update `class` from Erkul.

3. **Database Rebuilds & Refresh**:
   - Dropped existing PostgreSQL tables and re-ran both builders.
   - Executed [update_friendly_names.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/update_friendly_names.py).
   - Successfully filtered out **43** placeholder items (such as `COOL_S01_Template`, `COOL_Template`, `POWR_S01_Template`, and test weapons).

4. **Report Integration**:
   - Updated [generate_loadouts_report.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/generate_loadouts_report.py) to print the `Classification` column in default component tables.
   - Updated [export_loadouts_json.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/export_loadouts_json.py) to serialize the `"classification"` field.

---

## Verification Results

| Database | Ships Count | Ship Ports Count | Components Count | Default Loadout Rows | Placeholder Components |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **SQLite (`sc_database.db`)** | 193 | **5,194** | **722** | **3,706** | **0** |
| **PostgreSQL (`guild_db`)** | 193 | **5,194** | **722** | **3,706** | **0** |

---

## Key Files & Assets

- **Ship Default Loadouts Catalog**: [ship_default_loadouts.md](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/ship_default_loadouts.md)
- **Ship Default Loadouts JSON**: [ship_default_loadouts.json](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/ship_default_loadouts.json)
- **Pledge Ships Catalog**: [pledge_ships_report.md](file:///C:/Users/mpsoa/.gemini/antigravity/brain/9d2aa908-24a9-4436-b2e5-56f2fea32cff/pledge_ships_report.md) (Brain Artifact)
- **Database Build Scripts**: [build_sc_db.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db.py) and [build_sc_db_pg.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db_pg.py)
- **Update Translation & Classification Script**: [update_friendly_names.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/update_friendly_names.py)
