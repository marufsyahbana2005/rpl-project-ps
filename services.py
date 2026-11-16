"""
services.py — Lapisan Logika Bisnis & Layanan Data Exito Playbox
Memisahkan seluruh kueri SQL dan validasi bisnis dari routing controller app.py.
"""

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
