# GATUZ Egg Farm Management System

A desktop app for managing farm operations using Python, Tkinter, and SQLite. Nagsisimula pa lang? Tingnan ang [Mabilisang Gabay sa Filipino](QUICK_START_TL.md).

## Start here (Windows)

1. Install Python 3.12 or newer from [python.org](https://www.python.org/).
2. Download or clone this repository and extract it if you downloaded a ZIP.
3. Double-click **`START_GATUZ.bat`** from the repository root. Internet access is needed on first launch to install dependencies.
4. If the default account is still active, sign in with `admin` / `admin123` and change the password before entering real data. Admins can manage/reset accounts from **Users**; a self-service password change is not currently exposed in the navigation.

For step-by-step guidance, read [QUICK_START_TL.md](QUICK_START_TL.md).

## Dashboard

The refreshed dashboard is based on actual records in the existing SQLite database. It includes farm-selection cards, active chicken count, egg totals, sales and unpaid balances, daily production and monthly sales trends, egg-grade totals, and recent activity. The original application remains available in `app.py`; the launcher uses `dashboard_app.py` to render the refreshed dashboard while retaining the existing management screens.

The database does not currently record egg weight or historical flock counts. Therefore, the dashboard clearly shows average egg weight as not recorded and does not invent an age-based production percentage. The production chart displays recorded egg counts, not a fictional hen-day or week-of-age curve.

## Current functions

- Multiple farms and farm filtering
- Flock/batch records
- Egg production records by grade
- Inventory and stock movements
- Customers, sales, payments, and balances
- Expenses, dashboard summaries, and Excel/PDF report export
- Admin/staff user management
- Database backups and restore

No separate mortality/culling, morning/afternoon collection, hen-day production, egg-weight, or vaccination modules were added. Verify the current UI and schema before planning those features.

## Run manually

Open a command prompt in `GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/GATUZ_EGG_FARM_MANAGEMENT_SYSTEM/`, then run:

```bash
python -m pip install -r requirements.txt
python dashboard_app.py
```

Tkinter must be available in the Python installation. `BUILD_EXE.bat` builds a Windows onedir package; distribute the complete output folder and test it with a non-production database first.

## Protect your data

Use **Backup & restore → Create manual backup** and keep a separate copy in a secure location. Restore replaces the current database, so confirm the file and keep a safety copy first.

**Security warning:** this repository already contains tracked SQLite database/backup files. `.gitignore` only affects future untracked files; it does not remove existing tracked data or erase Git history. Review repository visibility and database contents before storing real business or customer data. Do not commit credentials.
