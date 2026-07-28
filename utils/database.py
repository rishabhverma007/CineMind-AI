import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "cinemaind.db"


def _connection():
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS favourites (movie_id INTEGER PRIMARY KEY, title TEXT, poster TEXT, saved_at TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, created_at TEXT)")
    return con


def toggle_favourite(movie: dict) -> bool:
    with _connection() as con:
        exists = con.execute("SELECT 1 FROM favourites WHERE movie_id=?", (movie["id"],)).fetchone()
        if exists:
            con.execute("DELETE FROM favourites WHERE movie_id=?", (movie["id"],))
            return False
        con.execute("INSERT INTO favourites VALUES (?,?,?,?)", (movie["id"], movie.get("title", ""), movie.get("poster_path", ""), datetime.now().isoformat()))
        return True


def favourites() -> list[dict]:
    with _connection() as con:
        rows = con.execute("SELECT movie_id,title,poster,saved_at FROM favourites ORDER BY saved_at DESC").fetchall()
    return [{"id": r[0], "title": r[1], "poster_path": r[2], "saved_at": r[3]} for r in rows]


def log_search(query: str) -> None:
    if query.strip():
        with _connection() as con: con.execute("INSERT INTO history(query,created_at) VALUES (?,?)", (query.strip(), datetime.now().isoformat()))
