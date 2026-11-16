"""
models.py — Lapisan Akses Basis Data SQLite untuk Exito Playbox
Mengelola koneksi SQLite, penegakan integritas foreign keys, dan inisialisasi skema.
"""

import os
import sqlite3

DATABASE_NAME = os.environ.get("DATABASE_NAME", "rental.db")
SCHEMA_PATH = os.path.join("docs", "desain", "schema.sql")


def get_db_connection(db_name=None):
    """
    Membuka koneksi ke basis data SQLite dengan penegakan Foreign Key
    dan row_factory untuk akses kolom berbasis nama (dict-like).
    """
    target_db = db_name or DATABASE_NAME
    conn = sqlite3.connect(target_db)
    conn.row_factory = sqlite3.Row
    # Aktifkan penegakan integritas referensial Foreign Key di SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_name=None, schema_file=None):
    """
    Menginisialisasi basis data dari berkas schema.sql bila tabel belum terbentuk.
    """
    target_db = db_name or DATABASE_NAME
    target_schema = schema_file or SCHEMA_PATH

    if not os.path.exists(target_schema):
        raise FileNotFoundError(f"Berkas skema tidak ditemukan pada: {target_schema}")

    conn = get_db_connection(target_db)
    with open(target_schema, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with conn:
        conn.executescript(schema_sql)
    conn.close()
    return True
