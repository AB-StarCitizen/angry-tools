# Implementation Plan - Component Filtering in Database and Reports

We will adjust the database build scripts (`build_sc_db.py` and `build_sc_db_pg.py`) to restrict both databases to only contain the component types matching the default loadout whitelist:
- Power Plants (`PowerPlant`)
- Shields (`Shield`)
- Quantum Drives (`QuantumDrive`)
- Coolers (`Cooler`)
- Radars (`Radar`)
- Weapons (`WeaponGun`)
- Missiles & Torpedoes (`Missile`)
- Missile Launchers / Racks (`MissileLauncher`)

This filtering will also propagate to ship ports, so only ports that accept these types or mount whitelisted default components are preserved.

---

## Proposed Changes

### Database Build Scripts

#### [MODIFY] [build_sc_db.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db.py)
- Filter out components during parsing from the source files using the whitelist of allowed types.
- Filter out ports in `parse_ships` if their accepted types do not match the whitelist and they do not host a whitelisted default component.

#### [MODIFY] [build_sc_db_pg.py](file:///C:/Users/mpsoa/Desktop/SC_4.8_data/build_sc_db_pg.py)
- Implement the identical filtering logic for components and ship ports to maintain SQLite/PostgreSQL schema and content symmetry.

### Database Rebuilding & Name Update

#### [RUN] Rebuild and Sync Commands
- Run `build_sc_db.py` to rebuild `sc_database.db`.
- Run `build_sc_db_pg.py` to rebuild PostgreSQL `guild_db` tables.
- Run `update_friendly_names.py` to fetch from Erkul API and update friendly names in both databases.

### Reports Regeneration

#### [RUN] Report Scripts
- Run `generate_loadouts_report.py` to compile `ship_default_loadouts.md`.
- Run `export_loadouts_json.py` to compile `ship_default_loadouts.json`.
- Run `generate_pledge_report.py` to compile `pledge_ships_report.md`.

---

## Verification Plan

### Database Queries & Count Checks
- Confirm SQLite and PostgreSQL counts:
  - 193 ships
  - 5,195 ship ports
  - 765 components
  - 3,707 default loadouts
- Check component name translation for `GLSN_BallisticGatling_S4` -> `Breakneck S4` and `GLSN_LaserRepeater_S3` -> `Tormenter S3` in both databases.

### Output Verification
- Verify that only the whitelisted component types are listed in `ship_default_loadouts.md` and `ship_default_loadouts.json`.
