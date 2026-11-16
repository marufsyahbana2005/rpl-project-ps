"""
services.py — Lapisan Logika Bisnis & Layanan Data Exito Playbox
Memisahkan seluruh kueri SQL dan validasi bisnis dari routing controller app.py.
"""

import sqlite3
from models import get_db_connection


def get_all_consoles(db_name=None):
    """
    Mengambil seluruh data unit konsol dari tabel consoles,
    diurutkan berdasarkan id secara menaik (ASC).
    """
    conn = get_db_connection(db_name)
    try:
        consoles = conn.execute(
            "SELECT id, kode_konsol, jenis_konsol, status FROM consoles ORDER BY id ASC;"
        ).fetchall()
        return consoles
    finally:
        conn.close()


def get_console_by_id(console_id, db_name=None):
    """
    Mengambil data satu unit konsol berdasarkan primary key id.
    Mengembalikan Row atau None jika tidak ditemukan.
    """
    conn = get_db_connection(db_name)
    try:
        console = conn.execute(
            "SELECT id, kode_konsol, jenis_konsol, status FROM consoles WHERE id = ?;",
            (console_id,),
        ).fetchone()
        return console
    finally:
        conn.close()


def create_console(kode_konsol, jenis_konsol, status="tersedia", db_name=None):
    """
    Memvalidasi dan menambahkan unit konsol baru ke tabel consoles.
    Mengembalikan tuple (success: bool, error_messages: list, console_id: int).
    """
    errors = []
    kode_clean = (kode_konsol or "").strip().upper()
    jenis_clean = (jenis_konsol or "").strip().upper()

    # Validasi 1: Wajib diisi dan batasan panjang
    if not kode_clean:
        errors.append("Kode konsol wajib diisi.")
    elif len(kode_clean) < 4:
        errors.append("Kode konsol minimal 4 karakter (misal: PS4-01).")

    # Validasi 2: Nilai jenis konsol harus sesuai batasan CHECK
    if jenis_clean not in ("PS3", "PS4", "PS5"):
        errors.append("Jenis konsol tidak valid. Pilihan hanya PS3, PS4, atau PS5.")

    # Validasi 3: Status harus valid
    if status not in ("tersedia", "terpakai", "maintenance"):
        errors.append("Status operasional tidak valid.")

    if errors:
        return False, errors, None

    conn = get_db_connection(db_name)
    try:
        # Validasi 4: Cek duplikasi kode_konsol (UNIQUE constraint)
        existing = conn.execute(
            "SELECT id FROM consoles WHERE kode_konsol = ?;",
            (kode_clean,),
        ).fetchone()

        if existing:
            errors.append(f"Kode konsol '{kode_clean}' sudah terdaftar di sistem.")
            return False, errors, None

        # SQL Berparameter untuk mencegah SQL Injection
        cursor = conn.execute(
            "INSERT INTO consoles (kode_konsol, jenis_konsol, status) VALUES (?, ?, ?);",
            (kode_clean, jenis_clean, status),
        )
        conn.commit()
        return True, [], cursor.lastrowid
    except sqlite3.IntegrityError as e:
        errors.append(f"Pelanggaran integritas basis data: {e}")
        return False, errors, None
    finally:
        conn.close()
