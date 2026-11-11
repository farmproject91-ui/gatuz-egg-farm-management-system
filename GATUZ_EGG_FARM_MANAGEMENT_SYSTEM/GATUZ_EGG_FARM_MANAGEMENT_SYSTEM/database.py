import os, sqlite3, hashlib, secrets, shutil
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
DB_PATH = os.path.join(DATA_DIR, "gatuz.db")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

def connect():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 180000).hex()
    return salt + "$" + digest

def verify_password(password, stored):
    try:
        salt, digest = stored.split("$", 1)
        return secrets.compare_digest(hash_password(password, salt).split("$",1)[1], digest)
    except Exception:
        return False

def init_db():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'staff', active INTEGER NOT NULL DEFAULT 1, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS farms(id INTEGER PRIMARY KEY, name TEXT NOT NULL, location TEXT DEFAULT '', notes TEXT DEFAULT '', archived INTEGER NOT NULL DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS flocks(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, batch_name TEXT NOT NULL, breed TEXT DEFAULT '', bird_count INTEGER NOT NULL DEFAULT 0, date_added TEXT NOT NULL, status TEXT DEFAULT 'Active', notes TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS production(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, day TEXT NOT NULL, jumbo INTEGER DEFAULT 0, xl INTEGER DEFAULT 0, large INTEGER DEFAULT 0, medium INTEGER DEFAULT 0, small INTEGER DEFAULT 0, peewee INTEGER DEFAULT 0, cracked INTEGER DEFAULT 0, damaged INTEGER DEFAULT 0, notes TEXT DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS inventory(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, name TEXT NOT NULL, category TEXT NOT NULL, unit TEXT DEFAULT 'pcs', quantity REAL DEFAULT 0, reorder_level REAL DEFAULT 0, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS stock_moves(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, item_id INTEGER NOT NULL REFERENCES inventory(id) ON DELETE CASCADE, move_type TEXT NOT NULL, quantity REAL NOT NULL, notes TEXT DEFAULT '', day TEXT DEFAULT CURRENT_DATE);
        CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, name TEXT NOT NULL, phone TEXT DEFAULT '', address TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL, day TEXT NOT NULL, grade TEXT NOT NULL, quantity REAL NOT NULL, unit_price REAL NOT NULL, total REAL NOT NULL, paid REAL DEFAULT 0, notes TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE, day TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, amount REAL NOT NULL, notes TEXT DEFAULT '');
        """)
        if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)", ("admin",hash_password("admin123"),"admin"))
        if c.execute("SELECT COUNT(*) FROM farms").fetchone()[0] == 0:
            c.execute("INSERT INTO farms(name,location,notes) VALUES(?,?,?)", ("Sample Farm","Edit this sample location","SAMPLE DATA — replace or delete this farm"))
        c.commit()

def backup_db(destination=None):
    if not os.path.exists(DB_PATH): return None
    if not destination:
        destination = os.path.join(BACKUP_DIR, "gatuz_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".db")
    shutil.copy2(DB_PATH, destination)
    return destination

def farm_rows(include_archived=False):
    with connect() as c:
        q = "SELECT * FROM farms" + ("" if include_archived else " WHERE archived=0") + " ORDER BY name"
        return c.execute(q).fetchall()

def farm_stats(farm_id=None):
    where, args = ("", []) if farm_id is None else (" WHERE farm_id=?", [farm_id])
    with connect() as c:
        if farm_id is None:
            chickens = c.execute("SELECT COALESCE(SUM(bird_count),0) FROM flocks WHERE status='Active'").fetchone()[0]
        else:
            chickens = c.execute("SELECT COALESCE(SUM(bird_count),0) FROM flocks WHERE farm_id=? AND status='Active'", args).fetchone()[0]
        eggs = c.execute("SELECT COALESCE(SUM(jumbo+xl+large+medium+small+peewee),0) FROM production"+where,args).fetchone()[0]
        cracked = c.execute("SELECT COALESCE(SUM(cracked),0) FROM production"+where,args).fetchone()[0]
        damaged = c.execute("SELECT COALESCE(SUM(damaged),0) FROM production"+where,args).fetchone()[0]
        sales = c.execute("SELECT COALESCE(SUM(total),0) FROM sales"+where,args).fetchone()[0]
        paid = c.execute("SELECT COALESCE(SUM(paid),0) FROM sales"+where,args).fetchone()[0]
        expenses = c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses"+where,args).fetchone()[0]
        return {"chickens":chickens,"eggs":eggs,"cracked":cracked,"damaged":damaged,"sales":sales,"paid":paid,"balance":sales-paid,"expenses":expenses,"profit":sales-expenses}

def recent_activity(farm_id=None, limit=12):
    with connect() as c:
        cond = "" if farm_id is None else " WHERE farm_id=?"
        arg = [] if farm_id is None else [farm_id]
        rows=[]
        for table, label, field in [("production","Egg collection","day"),("sales","Sale","day"),("expenses","Expense","day"),("stock_moves","Stock movement","day")]:
            for r in c.execute(f"SELECT {field} AS day, farm_id FROM {table}{cond} ORDER BY id DESC LIMIT ?", arg+[limit]):
                rows.append((r["day"], label, r["farm_id"]))
        names={r["id"]:r["name"] for r in farm_rows(True)}
        return sorted([(d, f"{label} — {names.get(fid,'Farm')}", fid) for d,label,fid in rows], reverse=True)[:limit]
