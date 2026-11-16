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

    if not kode_clean:
        errors.append("Kode konsol wajib diisi.")
    elif len(kode_clean) < 4:
        errors.append("Kode konsol minimal 4 karakter (misal: PS4-01).")

    if jenis_clean not in ("PS3", "PS4", "PS5"):
        errors.append("Jenis konsol tidak valid. Pilihan hanya PS3, PS4, atau PS5.")

    if status not in ("tersedia", "terpakai", "maintenance"):
        errors.append("Status operasional tidak valid.")

    if errors:
        return False, errors, None

    conn = get_db_connection(db_name)
    try:
        existing = conn.execute(
            "SELECT id FROM consoles WHERE kode_konsol = ?;",
            (kode_clean,),
        ).fetchone()

        if existing:
            errors.append(f"Kode konsol '{kode_clean}' sudah terdaftar di sistem.")
            return False, errors, None

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


def update_console(console_id, kode_konsol, jenis_konsol, status, db_name=None):
    """
    Memvalidasi dan memperbarui data unit konsol (F4).
    Mengembalikan tuple (success: bool, error_messages: list, status_code: int).
    """
    errors = []
    kode_clean = (kode_konsol or "").strip().upper()
    jenis_clean = (jenis_konsol or "").strip().upper()
    status_clean = (status or "").strip().lower()

    conn = get_db_connection(db_name)
    try:
        current = conn.execute(
            "SELECT id, kode_konsol, jenis_konsol, status FROM consoles WHERE id = ?;",
            (console_id,),
        ).fetchone()

        if not current:
            return False, ["Unit konsol tidak ditemukan di dalam sistem."], 404

        if not kode_clean:
            errors.append("Kode konsol wajib diisi.")
        elif len(kode_clean) < 4:
            errors.append("Kode konsol minimal 4 karakter.")

        if jenis_clean not in ("PS3", "PS4", "PS5"):
            errors.append("Jenis konsol harus salah satu dari: PS3, PS4, atau PS5.")

        # Pembatasan status manual: hanya 'tersedia' atau 'maintenance'
        if status_clean not in ("tersedia", "maintenance"):
            errors.append("Status manual hanya boleh 'tersedia' atau 'maintenance'.")

        if errors:
            return False, errors, 400

        # Cek apakah kode_konsol bentrok dengan unit konsol lain
        duplicate = conn.execute(
            "SELECT id FROM consoles WHERE kode_konsol = ? AND id != ?;",
            (kode_clean, console_id),
        ).fetchone()

        if duplicate:
            errors.append(f"Kode konsol '{kode_clean}' sudah digunakan oleh unit lain.")
            return False, errors, 400

        conn.execute(
            "UPDATE consoles SET kode_konsol = ?, jenis_konsol = ?, status = ? WHERE id = ?;",
            (kode_clean, jenis_clean, status_clean, console_id),
        )
        conn.commit()
        return True, [], 200
    finally:
        conn.close()


def delete_console(console_id, db_name=None):
    """
    Menghapus unit konsol (F5) dengan proteksi Foreign Key.
    Jika unit pernah dipakai dalam tabel transactions, penghapusan ditolak
    secara ramah (ON DELETE RESTRICT) tanpa menyebabkan crash aplikasi.
    Mengembalikan tuple (success: bool, message: str, status_code: int).
    """
    conn = get_db_connection(db_name)
    try:
        current = conn.execute(
            "SELECT id, kode_konsol FROM consoles WHERE id = ?;",
            (console_id,),
        ).fetchone()

        if not current:
            return False, "Unit konsol tidak ditemukan.", 404

        # Cek apakah unit konsol sedang atau pernah tercatat di transaksi sewa
        trx_count = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE console_id = ?;",
            (console_id,),
        ).fetchone()[0]

        if trx_count > 0:
            return (
                False,
                f"Unit '{current['kode_konsol']}' tidak dapat dihapus karena memiliki {trx_count} riwayat transaksi sewa. Ubah statusnya menjadi 'maintenance' sebagai gantinya.",
                400,
            )

        conn.execute("DELETE FROM consoles WHERE id = ?;", (console_id,))
        conn.commit()
        return (
            True,
            f"Unit konsol '{current['kode_konsol']}' berhasil dihapus dari sistem.",
            200,
        )
    except sqlite3.IntegrityError as e:
        return False, f"Gagal menghapus unit karena aturan integritas data: {e}", 400
    finally:
        conn.close()
