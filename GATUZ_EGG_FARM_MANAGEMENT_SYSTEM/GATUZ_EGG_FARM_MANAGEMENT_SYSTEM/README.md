# GATUZ EGG FARM MANAGEMENT SYSTEM

Offline-first Windows desktop application using Python, Tkinter, and SQLite. The original application modules are kept in this directory; repository-root launchers delegate here.

## Quick start (Windows)
1. Install Python 3.12 or newer from https://www.python.org/ and enable **Add Python to PATH**.
2. From the repository root, double-click `START_GATUZ.bat`, or double-click this directory's `START_GATUZ.bat`.
3. The first launch installs the dependencies listed in `requirements.txt` and starts the app.
4. The database is stored at `data/gatuz.db`. Change the seeded admin password immediately after signing in; the default account is for initial setup only and is not suitable for real farm data.

Manual run: open Command Prompt in this directory, install dependencies with `python -m pip install -r requirements.txt`, then run `python app.py`. Tkinter must be available in your Python installation.

## Existing features
- Multiple farms and per-farm filtering.
- Flock/batch records and active-bird totals.
- Daily egg collection and grade counts, including cracked and damaged eggs.
- Inventory, stock-in/stock-out movements, and low-stock indicators.
- Customers, sales, payments, balances, and receipt text.
- Expenses, dashboard summaries, and Excel/PDF exports.
- Admin/staff accounts and roles.
- Automatic daily database snapshots, manual backup, and restore.

No duplicate modules were added. Separate mortality/culling, morning/afternoon collection, hen-day production, and vaccination records are not claimed as current features; assess the existing schema and UI before adding future modules.

## Backup and restore
- Use **Backup & restore → Create manual backup** for an SQLite backup. The application also creates an automatic daily snapshot when first launched each day.
- Store a second copy securely outside the project/repository. Backups can contain private business data.
- For a manual filesystem copy, close the app first and copy `data/gatuz.db` and any required backup from `backups/`. Never copy a database while the app is writing to it.
- Restore with **Backup & restore → Restore from backup file**. Confirm the selected file carefully; the app asks for confirmation and creates a safety backup before replacement.

## Build an executable
Run `BUILD_EXE.bat`. PyInstaller builds an onedir package under `dist/GATUZ_EGG_FARM/`. Distribute the whole output directory. Test the packaged app and its data paths on a disposable copy before using it with production records.

## Database and security notes
The existing SQLite schema and records have been left untouched. This repository already contains tracked SQLite database/backup files. Ignore rules do not untrack existing files; do not assume those records are private. The owner should review repository visibility and arrange a separately reviewed removal/untracking process if the data must not be published. Do not commit credentials or production passwords. Change the seeded initial admin password before entering real data.
