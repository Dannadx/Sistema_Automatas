import csv
from pathlib import Path
from database import insert_log, query_logs

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exports"

def log_event(level, category, message, details=""):
    """Guarda el evento en SQLite y lo conserva después de cerrar el programa."""
    insert_log(level, category, message, details)

def export_logs(rows, file_path, format_name="csv"):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["id", "timestamp", "level", "category", "message", "details"]
    if format_name.lower() == "csv":
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for row in rows:
                writer.writerow([row[c] for c in columns])
    else:
        with path.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(
                    f"[{row['timestamp']}] [{row['level']}] "
                    f"[{row['category']}] {row['message']} | {row['details']}\n"
                )
    return path
