import sqlite3
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "regex_lab.db"

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                category TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)
        """)
        conn.commit()

def insert_log(level, category, message, details=""):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO logs(timestamp, level, category, message, details) VALUES (?, ?, ?, ?, ?)",
            (timestamp, level.upper(), category, message, str(details))
        )
        conn.commit()

def query_logs(level="Todos", category="Todos", search="", limit=2000):
    sql = "SELECT * FROM logs WHERE 1=1"
    params = []
    if level and level != "Todos":
        sql += " AND level = ?"
        params.append(level.upper())
    if category and category != "Todos":
        sql += " AND category = ?"
        params.append(category)
    if search:
        sql += " AND (message LIKE ? OR details LIKE ? OR category LIKE ?)"
        needle = f"%{search}%"
        params.extend([needle, needle, needle])
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(int(limit))
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()

def get_stats():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        errors = conn.execute("SELECT COUNT(*) FROM logs WHERE level IN ('ERROR','CRITICAL')").fetchone()[0]
        warnings = conn.execute("SELECT COUNT(*) FROM logs WHERE level='WARNING'").fetchone()[0]
        info = conn.execute("SELECT COUNT(*) FROM logs WHERE level='INFO'").fetchone()[0]
        return {"total": total, "errors": errors, "warnings": warnings, "info": info}

def clear_logs():
    with get_connection() as conn:
        conn.execute("DELETE FROM logs")
        conn.commit()
