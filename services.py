"""
services.py — Lapisan Logika Bisnis & Layanan Data Exito Playbox
Memisahkan seluruh kueri SQL dan validasi bisnis dari routing controller app.py.
Mencakup modul entitas pertama (consoles) dan entitas kedua (packages).
"""

import sqlite3
from models import get_db_connection


# ============================================================================
# 1. MODUL ENTITAS PERTAMA: CONSOLES (UNIT KONSOL PLAYSTATION)
# ============================================================================

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
    Memvalidasi dan menambahkan unit konsol baru ke tabel consoles (F3).
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

        if status_clean not in ("tersedia", "maintenance"):
            errors.append("Status manual hanya boleh 'tersedia' atau 'maintenance'.")

        if errors:
            return False, errors, 400

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
    """
    conn = get_db_connection(db_name)
    try:
        current = conn.execute(
            "SELECT id, kode_konsol FROM consoles WHERE id = ?;",
            (console_id,),
        ).fetchone()

        if not current:
            return False, "Unit konsol tidak ditemukan.", 404

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


# ============================================================================
# 2. MODUL ENTITAS KEDUA: PACKAGES (PAKET SEWA RENTAL) — LANGKAH 14
# ============================================================================

def get_all_packages(db_name=None):
    """
    Mengambil seluruh daftar paket sewa dari tabel packages.
    """
    conn = get_db_connection(db_name)
    try:
        packages = conn.execute(
            "SELECT id, nama_paket, jenis_konsol, durasi_menit, harga, is_active FROM packages ORDER BY id ASC;"
        ).fetchall()
        return packages
    finally:
        conn.close()


def get_package_by_id(package_id, db_name=None):
    """
    Mengambil data satu paket sewa berdasarkan id.
    """
    conn = get_db_connection(db_name)
    try:
        package = conn.execute(
            "SELECT id, nama_paket, jenis_konsol, durasi_menit, harga, is_active FROM packages WHERE id = ?;",
            (package_id,),
        ).fetchone()
        return package
    finally:
        conn.close()


def create_package(nama_paket, jenis_konsol, durasi_menit, harga, is_active=1, db_name=None):
    """
    Memvalidasi dan menambahkan paket sewa baru ke tabel packages.
    Validasi: durasi_menit > 0, harga >= 0, nama unik, jenis konsol valid.
    """
    errors = []
    nama_clean = (nama_paket or "").strip()
    jenis_clean = (jenis_konsol or "").strip().upper()

    if not nama_clean:
        errors.append("Nama paket sewa wajib diisi.")

    if jenis_clean not in ("PS3", "PS4", "PS5"):
        errors.append("Jenis konsol tidak valid. Pilih PS3, PS4, atau PS5.")

    try:
        durasi_val = int(durasi_menit)
        if durasi_val <= 0:
            errors.append("Durasi sewa harus lebih besar dari 0 menit.")
    except (ValueError, TypeError):
        errors.append("Durasi sewa harus berupa angka menit bulat.")

    try:
        harga_val = int(harga)
        if harga_val < 0:
            errors.append("Harga sewa tidak boleh bernilai negatif.")
    except (ValueError, TypeError):
        errors.append("Harga sewa harus berupa angka Rupiah yang valid.")

    if errors:
        return False, errors, None

    conn = get_db_connection(db_name)
    try:
        existing = conn.execute(
            "SELECT id FROM packages WHERE nama_paket = ?;",
            (nama_clean,),
        ).fetchone()

        if existing:
            errors.append(f"Nama paket '{nama_clean}' sudah digunakan.")
            return False, errors, None

        cursor = conn.execute(
            "INSERT INTO packages (nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (?, ?, ?, ?, ?);",
            (nama_clean, jenis_clean, durasi_val, harga_val, 1 if is_active else 0),
        )
        conn.commit()
        return True, [], cursor.lastrowid
    except sqlite3.IntegrityError as e:
        errors.append(f"Pelanggaran integritas basis data: {e}")
        return False, errors, None
    finally:
        conn.close()


def update_package(package_id, nama_paket, jenis_konsol, durasi_menit, harga, is_active=1, db_name=None):
    """
    Memvalidasi dan memperbarui paket sewa yang ada.
    """
    errors = []
    nama_clean = (nama_paket or "").strip()
    jenis_clean = (jenis_konsol or "").strip().upper()

    conn = get_db_connection(db_name)
    try:
        current = conn.execute(
            "SELECT id FROM packages WHERE id = ?;", (package_id,)
        ).fetchone()

        if not current:
            return False, ["Paket sewa tidak ditemukan."], 404

        if not nama_clean:
            errors.append("Nama paket sewa wajib diisi.")

        if jenis_clean not in ("PS3", "PS4", "PS5"):
            errors.append("Jenis konsol harus salah satu dari: PS3, PS4, atau PS5.")

        try:
            durasi_val = int(durasi_menit)
            if durasi_val <= 0:
                errors.append("Durasi sewa harus lebih besar dari 0 menit.")
        except (ValueError, TypeError):
            errors.append("Durasi sewa harus berupa angka menit bulat.")

        try:
            harga_val = int(harga)
            if harga_val < 0:
                errors.append("Harga sewa tidak boleh bernilai negatif.")
        except (ValueError, TypeError):
            errors.append("Harga sewa harus berupa angka Rupiah yang valid.")

        if errors:
            return False, errors, 400

        duplicate = conn.execute(
            "SELECT id FROM packages WHERE nama_paket = ? AND id != ?;",
            (nama_clean, package_id),
        ).fetchone()

        if duplicate:
            errors.append(f"Nama paket '{nama_clean}' sudah digunakan oleh paket lain.")
            return False, errors, 400

        conn.execute(
            "UPDATE packages SET nama_paket = ?, jenis_konsol = ?, durasi_menit = ?, harga = ?, is_active = ? WHERE id = ?;",
            (nama_clean, jenis_clean, durasi_val, harga_val, 1 if is_active else 0, package_id),
        )
        conn.commit()
        return True, [], 200
    finally:
        conn.close()


def delete_package(package_id, db_name=None):
    """
    Menghapus paket sewa dengan proteksi Foreign Key.
    Jika paket sudah memiliki transaksi sewa, penghapusan ditolak ramah.
    """
    conn = get_db_connection(db_name)
    try:
        current = conn.execute(
            "SELECT id, nama_paket FROM packages WHERE id = ?;", (package_id,)
        ).fetchone()

        if not current:
            return False, "Paket sewa tidak ditemukan.", 404

        trx_count = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE package_id = ?;", (package_id,)
        ).fetchone()[0]

        if trx_count > 0:
            return (
                False,
                f"Paket '{current['nama_paket']}' tidak dapat dihapus karena digunakan pada {trx_count} riwayat transaksi sewa. Ubah statusnya menjadi 'Nonaktif' sebagai gantinya.",
                400,
            )

        conn.execute("DELETE FROM packages WHERE id = ?;", (package_id,))
        conn.commit()
        return True, f"Paket sewa '{current['nama_paket']}' berhasil dihapus dari sistem.", 200
    except sqlite3.IntegrityError as e:
        return False, f"Gagal menghapus paket: {e}", 400
    finally:
        conn.close()
