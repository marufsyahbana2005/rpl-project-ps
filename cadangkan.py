"""
cadangkan.py — Skrip Pencadangan Basis Data SQLite Exito Playbox
Menggunakan SQLite Online Backup API (conn.backup) untuk menjamin konsistensi data
bahkan saat aplikasi sedang berjalan dan melayani transaksi aktif.
"""

import os
import sqlite3
from datetime import datetime

# Ambil lokasi basis data sumber dari variabel lingkungan TOKO_DB atau fallback DATABASE_NAME
SOURCE_DB = os.environ.get("TOKO_DB", os.environ.get("DATABASE_NAME", "rental.db"))
BACKUP_DIR = "cadangan"


def backup_database(source_db=None, backup_dir=None):
    """
    Melakukan pencadangan basis data SQLite ke direktori cadangan dengan stempel waktu.
    Mengembalikan path file cadangan yang berhasil dibuat.
    """
    src = source_db or SOURCE_DB
    dst_dir = backup_dir or BACKUP_DIR

    if not os.path.exists(src):
        raise FileNotFoundError(f"Basis data sumber tidak ditemukan pada: {src}")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"rental_backup_{timestamp}.db"
    backup_path = os.path.join(dst_dir, backup_filename)

    src_conn = sqlite3.connect(src)
    dst_conn = sqlite3.connect(backup_path)

    try:
        # Gunakan API backup bawaan SQLite
        src_conn.backup(dst_conn)
        print(f"[SUKSES] Pencadangan basis data '{src}' berhasil dibuat pada: '{backup_path}'")
        return backup_path
    finally:
        dst_conn.close()
        src_conn.close()


if __name__ == "__main__":
    backup_database()
