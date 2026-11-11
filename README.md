# GATUZ Egg Farm Management System

Offline-first Windows desktop application built with Python, Tkinter, and SQLite. The existing application is preserved in `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/`; the root-level batch files are convenience launchers for that project directory.

## Windows setup

1. Install Python 3.12 or newer from [python.org](https://www.python.org/), including the option to add Python to PATH.
2. From the repository root, double-click `START_GATUZ.bat`. It installs the application's dependencies and launches the existing app.
3. The application stores its working database at `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/data/gatuz.db`.
4. Change the initial admin password immediately after signing in. The application currently seeds a default `admin` account; do not use that account/password for production data without changing it.

To run manually, open Command Prompt in the nested project directory and run `python app.py` (install dependencies first using `python -m pip install -r requirements.txt`). Tkinter must be available in the Python installation.

## Existing functionality

This setup preserves the application's existing modules and SQLite schema. Current functionality includes multiple farms, flock/batch records, egg collection by grade, inventory and stock movements, customers, sales and payments, expenses, dashboard summaries, Excel/PDF exports, user roles, and database backup/restore. This setup does not add separate mortality/culling, morning/afternoon collection, hen-day production, or vaccination modules; check the existing application before planning future integration so features are not duplicated.

## Back up and restore your data

- Use **Backup & restore → Create manual backup** in the application for a consistent SQLite backup. The app also makes a daily snapshot at launch.
- Keep backups in a secure location separate from this repository and test that they can be opened/restored.
- To copy the database manually, close the application first, then copy `data/gatuz.db` and the desired files from `backups/` to a secure location. Do not copy a live SQLite database while it is being written.
- Restore through **Backup & restore → Restore from backup file**. The app asks before replacing current data and creates a safety copy first. Verify the selected backup before confirming.

## Build a Windows executable

Double-click `BUILD_EXE.bat` from the repository root. The build uses PyInstaller and places its output under the nested project's `dist/GATUZ_EGG_FARM/` directory. Distribute the complete output folder, not only the executable. Verify data and backup locations on a separate test copy before using a packaged build with production records.

## Security and repository data warning

`.gitignore` excludes local SQLite databases, backups, Python caches, build output, and credentials from future additions. **It does not remove files already tracked by Git.** At setup time, the repository already contained `data/gatuz.db` and a database backup under `backups/`; these tracked files have not been deleted or altered, to avoid losing existing records. Treat the repository as containing database data, restrict access as appropriate, and have the repository owner safely remove/untrack these files in a separate reviewed change if they must not be published. Never commit real passwords, API keys, or other private credentials. The app's seeded default login is not a secure production credential.

## Project layout

- `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/app.py` — existing desktop application
- `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/database.py` — existing SQLite schema and database helpers
- `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/README.md` — application-specific usage notes
- Root `START_GATUZ.bat` and `BUILD_EXE.bat` — launch/build wrappers
- Root `requirements.txt` — references the application's dependency list
