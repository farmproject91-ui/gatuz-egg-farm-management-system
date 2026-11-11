# GATUZ EGG FARM MANAGEMENT SYSTEM

Offline-first Windows desktop application using Python, Tkinter/CustomTkinter-compatible widgets, and SQLite.

## Quick start (Windows)
1. Install **Python 3.12 or newer** from https://www.python.org/ and enable **Add Python to PATH**.
2. Extract this ZIP to a normal folder (not inside the ZIP).
3. Double-click `START_GATUZ.bat`. It installs dependencies and starts the app.
4. First login: **admin** / **admin123**. Change this password immediately from **Users**.

The SQLite database is created automatically at `data/gatuz.db`. The app works offline after dependencies are installed.

## Run from Python IDLE
1. Open IDLE (Python 3.12+).
2. Choose File > Open, then open `app.py` from this extracted folder.
3. Press F5 (Run Module). Do not run it while another copy is open.

## Build a Windows application
Double-click `BUILD_EXE.bat` after installing Python. The build is placed in `dist/GATUZ_EGG_FARM/`.
This uses PyInstaller `--onedir` for reliability. Copy the entire output folder, not only the EXE.
Keep `data/` and `backups/` beside the EXE/app folder. For a portable copy, close the app and copy the whole project folder.

## Features
- Multiple farms: create, edit, archive, restore, and delete (delete requires confirmation).
- Combined dashboard and per-farm filtering, including production and sales charts.
- Chicken flock/batch records with active-bird totals.
- Daily egg collection by grade, cracked and damaged counts.
- Inventory items, stock-in/stock-out movements, and low-stock indicators.
- Customers, egg sales, payment status, outstanding balances, and printable receipt text.
- Categorized expenses and basic profit/loss summary.
- Admin/staff login and role restrictions.
- Automatic daily database snapshots on launch, manual backup, and restore from a SQLite backup.
- Excel and PDF report export where the relevant libraries are installed.

## Important notes
- This is a local single-computer application, not a cloud-sync or multi-user network database.
- Default credentials are for first setup only. Change the admin password before entering real business data.
- Backups are stored in `backups/`. Keep a separate copy on another drive regularly.
- Sample starter farm is labeled **Sample Farm** and may be edited or deleted.
- Financial summary is a simple cash/accounting overview: sales minus recorded expenses. Inventory purchases should be recorded as expenses if you want them included in profit.
