"""
BookIQ — SQLite Database Layer
Stores users, books, summaries, and access logs.
"""

import os
import sqlite3
import hashlib
import secrets
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/bookiq.db")


# ═══════════════════════════════════════════════════════════════════════════════
#  CONNECTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# ═══════════════════════════════════════════════════════════════════════════════
#  SCHEMA INITIALISATION
# ═══════════════════════════════════════════════════════════════════════════════

def init_db():
    conn = get_conn()
    cur  = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT    UNIQUE NOT NULL,
        password_hash TEXT  NOT NULL,
        role        TEXT    NOT NULL DEFAULT 'user',   -- 'admin' | 'user'
        created_at  TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS books (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL REFERENCES users(id),
        title       TEXT    NOT NULL,
        author      TEXT,
        tags        TEXT,
        raw_text    TEXT    NOT NULL,
        word_count  INTEGER,
        language    TEXT,
        uploaded_at TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS summaries (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id      INTEGER NOT NULL REFERENCES books(id),
        user_id      INTEGER NOT NULL REFERENCES users(id),
        summary_text TEXT    NOT NULL,
        key_ideas    TEXT,
        keywords     TEXT,
        length_pref  TEXT,
        style_pref   TEXT,
        rouge_f1     REAL,
        compression  REAL,
        created_at   TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS access_logs (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER REFERENCES users(id),
        action     TEXT    NOT NULL,
        detail     TEXT,
        timestamp  TEXT    NOT NULL
    );
    """)
    conn.commit()

    # Seed default accounts if not present
    _seed_users(cur, conn)
    conn.close()


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _seed_users(cur, conn):
    now = datetime.now().isoformat()
    defaults = [
        ("admin", "admin123", "admin"),
        ("raghav", "raghav123", "user"),
        ("demo",   "demo123",  "user"),
    ]
    for username, password, role in defaults:
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role, created_at) VALUES (?,?,?,?)",
            (username, _hash(password), role, now),
        )
    conn.commit()


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════════════════════════

def authenticate(username: str, password: str):
    """Returns user row dict or None."""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, _hash(password)),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def register_user(username: str, password: str, role: str = "user") -> bool:
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?,?,?,?)",
            (username, _hash(password), role, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id, username, role, created_at FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#  BOOKS
# ═══════════════════════════════════════════════════════════════════════════════

def save_book(user_id, title, author, tags, raw_text, word_count, language) -> int:
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO books (user_id, title, author, tags, raw_text,
           word_count, language, uploaded_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (user_id, title, author, tags, raw_text, word_count, language,
         datetime.now().isoformat()),
    )
    book_id = cur.lastrowid
    conn.commit()
    conn.close()
    return book_id


def get_books(user_id=None, search: str = "", role: str = "user"):
    conn = get_conn()
    if role == "admin":
        query = "SELECT b.*, u.username FROM books b JOIN users u ON b.user_id=u.id"
        params = []
    else:
        query = "SELECT b.*, u.username FROM books b JOIN users u ON b.user_id=u.id WHERE b.user_id=?"
        params = [user_id]

    if search:
        sep = " AND " if params else " WHERE "
        query += f"{sep}(b.title LIKE ? OR b.author LIKE ? OR b.tags LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]

    query += " ORDER BY b.uploaded_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_book(book_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_book(book_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM summaries WHERE book_id=?", (book_id,))
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
#  SUMMARIES
# ═══════════════════════════════════════════════════════════════════════════════

def save_summary(book_id, user_id, summary_text, key_ideas, keywords,
                 length_pref, style_pref, rouge_f1, compression) -> int:
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO summaries
           (book_id, user_id, summary_text, key_ideas, keywords,
            length_pref, style_pref, rouge_f1, compression, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (book_id, user_id, summary_text,
         "\n".join(key_ideas) if isinstance(key_ideas, list) else key_ideas,
         ", ".join(keywords)  if isinstance(keywords,  list) else keywords,
         length_pref, style_pref, rouge_f1, compression,
         datetime.now().isoformat()),
    )
    sid = cur.lastrowid
    conn.commit()
    conn.close()
    return sid


def get_summaries(user_id=None, book_id=None, role="user"):
    conn = get_conn()
    if role == "admin":
        query = """SELECT s.*, b.title, b.author, u.username
                   FROM summaries s
                   JOIN books b ON s.book_id=b.id
                   JOIN users u ON s.user_id=u.id"""
        params = []
    else:
        query = """SELECT s.*, b.title, b.author, u.username
                   FROM summaries s
                   JOIN books b ON s.book_id=b.id
                   JOIN users u ON s.user_id=u.id
                   WHERE s.user_id=?"""
        params = [user_id]

    if book_id:
        sep = " AND " if params else " WHERE "
        query += f"{sep} s.book_id=?"
        params.append(book_id)

    query += " ORDER BY s.created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
#  ACCESS LOG
# ═══════════════════════════════════════════════════════════════════════════════

def log_action(user_id, action: str, detail: str = ""):
    conn = get_conn()
    conn.execute(
        "INSERT INTO access_logs (user_id, action, detail, timestamp) VALUES (?,?,?,?)",
        (user_id, action, detail, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_logs(limit: int = 100):
    conn = get_conn()
    rows = conn.execute(
        """SELECT l.*, u.username FROM access_logs l
           LEFT JOIN users u ON l.user_id=u.id
           ORDER BY l.timestamp DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Init on import ────────────────────────────────────────────────────────────
init_db()
