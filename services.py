"""
services.py — Lapisan Logika Bisnis & Layanan Data Exito Playbox
Memisahkan seluruh kueri SQL dan validasi bisnis dari routing controller app.py.
Mencakup:
1. Modul Entitas Pertama (consoles)
2. Modul Entitas Kedua (packages)
3. Modul Entitas Berelasi & Transaksi Atomik (transactions) — Jobsheet 10
"""

import re
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
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


def get_available_consoles(db_name=None):
    """
    Mengambil daftar unit konsol yang berstatus 'tersedia' untuk pilihan sewa.
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, kode_konsol, jenis_konsol, status FROM consoles WHERE status = 'tersedia' ORDER BY kode_konsol ASC;"
        ).fetchall()
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
# 2. MODUL ENTITAS KEDUA: PACKAGES (PAKET SEWA RENTAL)
# ============================================================================

def get_all_packages(db_name=None):
    """
    Mengambil seluruh daftar paket sewa dari tabel packages.
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, nama_paket, jenis_konsol, durasi_menit, harga, is_active FROM packages ORDER BY id ASC;"
        ).fetchall()
    finally:
        conn.close()


def get_active_packages(db_name=None):
    """
    Mengambil daftar paket sewa yang berstatus aktif (is_active = 1) untuk pilihan sewa.
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, nama_paket, jenis_konsol, durasi_menit, harga FROM packages WHERE is_active = 1 ORDER BY jenis_konsol ASC, durasi_menit ASC;"
        ).fetchall()
    finally:
        conn.close()


def get_package_by_id(package_id, db_name=None):
    """
    Mengambil data satu paket sewa berdasarkan id.
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, nama_paket, jenis_konsol, durasi_menit, harga, is_active FROM packages WHERE id = ?;",
            (package_id,),
        ).fetchone()
    finally:
        conn.close()


def create_package(nama_paket, jenis_konsol, durasi_menit, harga, is_active=1, db_name=None):
    """
    Memvalidasi dan menambahkan paket sewa baru ke tabel packages.
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


# ============================================================================
# 3. MODUL ENTITAS BERELASI: TRANSACTIONS & TRANSAKSI ATOMIK (JOBSHEET 10)
# ============================================================================

def get_all_transactions(q=None, status_bayar=None, jenis_konsol=None, db_name=None):
    """
    Mengambil daftar seluruh transaksi sewa dengan kueri JOIN ke tabel consoles,
    packages, dan users untuk menyajikan informasi induk secara lengkap.
    Mendukung parameter pencarian (q) dan penyaringan (status_bayar, jenis_konsol).
    """
    conn = get_db_connection(db_name)
    try:
        sql = """
            SELECT 
                t.id AS id_transaksi,
                t.nama_pelanggan,
                t.waktu_mulai,
                t.waktu_selesai,
                t.status_bayar,
                c.id AS id_konsol,
                c.kode_konsol,
                c.jenis_konsol,
                c.status AS status_konsol_saat_ini,
                p.id AS id_paket,
                p.nama_paket,
                p.durasi_menit,
                p.harga AS harga_paket,
                u.id AS id_user,
                u.username AS nama_kasir,
                f.menit_terlambat,
                f.biaya_denda
            FROM transactions t
            JOIN consoles c ON t.console_id = c.id
            JOIN packages p ON t.package_id = p.id
            JOIN users u ON t.user_id = u.id
            LEFT JOIN fines f ON t.id = f.transaction_id
            WHERE 1=1
        """
        params = []

        # Sesi 2 / Langkah 9: Pencarian dengan LIKE berparameter dan escape karakter khusus
        if q:
            # Escape literal backslash, percent, dan underscore
            safe_q = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            sql += """ AND (
                t.nama_pelanggan LIKE ? ESCAPE '\\' 
                OR c.kode_konsol LIKE ? ESCAPE '\\'
                OR p.nama_paket LIKE ? ESCAPE '\\'
            )"""
            search_param = f"%{safe_q}%"
            params.extend([search_param, search_param, search_param])

        # Sesi 2 / Langkah 10: Penyaringan status bayar
        if status_bayar and status_bayar in ("lunas", "open_bill", "batal"):
            sql += " AND t.status_bayar = ?"
            params.append(status_bayar)

        # Sesi 2 / Langkah 10: Penyaringan jenis konsol
        if jenis_konsol and jenis_konsol in ("PS3", "PS4", "PS5"):
            sql += " AND c.jenis_konsol = ?"
            params.append(jenis_konsol)

        sql += " ORDER BY t.id DESC;"
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def get_transaction_by_id(transaction_id, db_name=None):
    """
    Mengambil detail satu transaksi sewa lengkap dengan data relasi induk dan informasi denda jika ada.
    """
    conn = get_db_connection(db_name)
    try:
        sql = """
            SELECT 
                t.id AS id_transaksi,
                t.nama_pelanggan,
                t.waktu_mulai,
                t.waktu_selesai,
                t.status_bayar,
                c.id AS id_konsol,
                c.kode_konsol,
                c.jenis_konsol,
                p.id AS id_paket,
                p.nama_paket,
                p.durasi_menit,
                p.harga AS harga_paket,
                u.id AS id_user,
                u.username AS nama_kasir,
                f.menit_terlambat,
                f.biaya_denda
            FROM transactions t
            JOIN consoles c ON t.console_id = c.id
            JOIN packages p ON t.package_id = p.id
            JOIN users u ON t.user_id = u.id
            LEFT JOIN fines f ON t.id = f.transaction_id
            WHERE t.id = ?;
        """
        return conn.execute(sql, (transaction_id,)).fetchone()
    finally:
        conn.close()


def _validate_transaction_payload(nama_pelanggan, console_id, package_id, status_bayar="open_bill"):
    """
    Fungsi bantuan refactoring (Langkah 13):
    Memvalidasi dan mensanitasi masukan formulir pembukaan transaksi sewa konsol.
    Mengembalikan tuple: (is_valid: bool, errors: list, nama_clean: str, c_id: int|None, p_id: int|None, status_bayar_clean: str)
    """
    errors = []
    nama_clean = (nama_pelanggan or "").strip()
    status_bayar_clean = (status_bayar or "open_bill").strip().lower()

    if not nama_clean:
        errors.append("Nama pelanggan wajib diisi.")
    elif len(nama_clean) < 2:
        errors.append("Nama pelanggan minimal 2 karakter.")

    # Validasi dan sanitasi input induk unit konsol
    try:
        c_id = int(console_id)
    except (ValueError, TypeError):
        errors.append("Pilih unit konsol yang valid dari daftar.")
        c_id = None

    # Validasi dan sanitasi input induk paket sewa
    try:
        p_id = int(package_id)
    except (ValueError, TypeError):
        errors.append("Pilih paket sewa yang valid dari daftar.")
        p_id = None

    if status_bayar_clean not in ("lunas", "open_bill"):
        status_bayar_clean = "open_bill"

    is_valid = len(errors) == 0
    return is_valid, errors, nama_clean, c_id, p_id, status_bayar_clean


def create_transaction(nama_pelanggan, console_id, package_id, status_bayar="open_bill", user_id=1, db_name=None):
    """
    Langkah 4 & 5 (Siklus 2 & 3): Form Tambah dengan Pilihan Induk & Transaksi Atomik Multi-Tabel.
    Dalam satu koneksi SQLite (with conn:), fungsi ini:
    1. Memvalidasi ketersediaan unit konsol dan keaktifan paket sewa.
    2. Menambahkan baris ke tabel transactions.
    3. Mengubah status unit konsol terkait menjadi 'terpakai'.
    Jika terjadi kegagalan atau data induk tidak ada, seluruh transaksi di-rollback secara otomatis.
    """
    is_valid, errors, nama_clean, c_id, p_id, status_bayar_clean = _validate_transaction_payload(
        nama_pelanggan=nama_pelanggan,
        console_id=console_id,
        package_id=package_id,
        status_bayar=status_bayar,
    )

    if not is_valid:
        return False, errors, None

    conn = get_db_connection(db_name)
    try:
        # Verifikasi keberadaan dan ketersediaan unit konsol induk
        console = conn.execute(
            "SELECT id, kode_konsol, status FROM consoles WHERE id = ?;", (c_id,)
        ).fetchone()

        if not console:
            errors.append(f"Unit konsol dengan ID #{c_id} tidak ditemukan di sistem.")
            return False, errors, None

        if console["status"] != "tersedia":
            errors.append(
                f"Unit '{console['kode_konsol']}' sedang tidak tersedia (status saat ini: '{console['status']}'). Pilih konsol lain."
            )
            return False, errors, None

        # Verifikasi keberadaan dan keaktifan paket sewa induk
        package = conn.execute(
            "SELECT id, nama_paket, is_active FROM packages WHERE id = ?;", (p_id,)
        ).fetchone()

        if not package:
            errors.append(f"Paket sewa dengan ID #{p_id} tidak ditemukan di sistem.")
            return False, errors, None

        if package["is_active"] != 1:
            errors.append(f"Paket sewa '{package['nama_paket']}' sedang nonaktif.")
            return False, errors, None

        # Verifikasi user kasir
        user = conn.execute("SELECT id FROM users WHERE id = ?;", (user_id,)).fetchone()
        if not user:
            # Otomatis pastikan kasir default tersedia
            conn.execute(
                "INSERT OR IGNORE INTO users (id, username, password_hash, role) VALUES (?, 'kasir_andi', 'hash123', 'kasir');",
                (user_id,)
            )

        # ====================================================================
        # EKSEKUSI TRANSAKSI ATOMIK (Langkah 5)
        # Dua tabel berubah bersama: transactions bertambah, consoles terpakai
        # ====================================================================
        with conn:
            # 1. Masukkan baris baru ke transactions
            cur = conn.execute(
                """
                INSERT INTO transactions (nama_pelanggan, user_id, console_id, package_id, waktu_mulai, status_bayar)
                VALUES (?, ?, ?, ?, datetime('now', 'localtime'), ?);
                """,
                (nama_clean, user_id, c_id, p_id, status_bayar_clean),
            )
            new_trx_id = cur.lastrowid

            # 2. Dampak pada tabel lain: ubah status konsol menjadi 'terpakai'
            conn.execute(
                "UPDATE consoles SET status = 'terpakai' WHERE id = ?;",
                (c_id,),
            )

        return True, [], new_trx_id
    except sqlite3.IntegrityError as e:
        errors.append(f"Pelanggaran integritas referensial: {e}")
        return False, errors, None
    finally:
        conn.close()


def finish_transaction(transaction_id, force_menit_terlambat=None, db_name=None):
    """
    Tugas Lanjutan (Langkah 16): Modul Penghentian Sesi Sewa & Perhitungan Denda.
    Menyelesaikan sesi sewa PlayStation:
    1. Mencatat waktu_selesai = datetime('now', 'localtime') dan status_bayar = 'lunas'.
    2. Mengembalikan status konsol dari 'terpakai' menjadi 'tersedia'.
    3. Mengkalkulasi durasi aktual; jika terlambat melebihi toleransi (5 menit),
       hitung denda (Rp 1.000 / menit) dan simpan ke tabel fines.
    """
    conn = get_db_connection(db_name)
    try:
        # Ambil data transaksi beserta konsol dan paket
        sql = """
            SELECT 
                t.id, t.nama_pelanggan, t.waktu_mulai, t.waktu_selesai, t.status_bayar,
                t.console_id, t.package_id,
                c.kode_konsol, c.status AS status_konsol,
                p.nama_paket, p.durasi_menit, p.harga AS harga_paket
            FROM transactions t
            JOIN consoles c ON t.console_id = c.id
            JOIN packages p ON t.package_id = p.id
            WHERE t.id = ?;
        """
        trx = conn.execute(sql, (transaction_id,)).fetchone()

        if not trx:
            return False, "Sesi transaksi sewa tidak ditemukan.", 404

        if trx["waktu_selesai"] is not None:
            return False, f"Sesi sewa #{transaction_id} untuk '{trx['nama_pelanggan']}' sudah diselesaikan sebelumnya.", 400

        # Kalkulasi durasi aktual vs durasi paket
        if force_menit_terlambat is not None:
            menit_terlambat = max(0, int(force_menit_terlambat))
        else:
            diff_row = conn.execute(
                "SELECT CAST((strftime('%s', datetime('now', 'localtime')) - strftime('%s', ?)) / 60 AS INTEGER) AS durasi_berjalan;",
                (trx["waktu_mulai"],)
            ).fetchone()
            durasi_berjalan = diff_row["durasi_berjalan"] if (diff_row and diff_row["durasi_berjalan"] is not None) else 0

            # Aturan toleransi keterlambatan (grace period): 5 menit
            if durasi_berjalan > (trx["durasi_menit"] + 5):
                menit_terlambat = durasi_berjalan - trx["durasi_menit"]
            else:
                menit_terlambat = 0

        # Tarif denda: Rp 1.000 per menit keterlambatan
        biaya_denda = menit_terlambat * 1000

        # Eksekusi atomik multi-tabel
        with conn:
            # 1. Update status transaksi sewa
            conn.execute(
                "UPDATE transactions SET waktu_selesai = datetime('now', 'localtime'), status_bayar = 'lunas' WHERE id = ?;",
                (transaction_id,)
            )

            # 2. Kembalikan unit konsol ke status 'tersedia'
            conn.execute(
                "UPDATE consoles SET status = 'tersedia' WHERE id = ?;",
                (trx["console_id"],)
            )

            # 3. Catat denda jika ada keterlambatan
            if menit_terlambat > 0:
                conn.execute(
                    "INSERT INTO fines (transaction_id, menit_terlambat, biaya_denda) VALUES (?, ?, ?);",
                    (transaction_id, menit_terlambat, biaya_denda)
                )

        pesan_sukses = f"Sesi sewa #{transaction_id} ({trx['nama_pelanggan']}) berhasil diselesaikan. Unit '{trx['kode_konsol']}' kini TERSEDIA kembali."
        if menit_terlambat > 0:
            pesan_sukses += f" Terlambat {menit_terlambat} menit. Denda: Rp {biaya_denda:,}."

        return True, pesan_sukses, 200
    except sqlite3.IntegrityError as e:
        return False, f"Galat integritas basis data saat menyelesaikan sewa: {e}", 400
    finally:
        conn.close()


# ============================================================================
# 4. MODUL ENTITAS PENGGUNA & AUTENTIKASI: USERS (JOBSHEET 11)
# ============================================================================

def create_user(username, password, role="kasir", is_active=1, db_name=None):
    """
    Langkah 3 (Siklus 1): Mendaftarkan akun pengguna baru dengan kata sandi ter-hash.
    Aturan:
    - Username: Wajib diisi, minimal 3 karakter, alfanumerik atau garis bawah (_).
    - Password: Wajib diisi, minimal 6 karakter. Di-hash menggunakan scrypt/pbkdf2 ber-salt.
    - Role: Wajib salah satu dari ('kasir', 'owner').
    """
    errors = []
    user_clean = (username or "").strip().lower()
    pass_clean = password or ""
    role_clean = (role or "kasir").strip().lower()

    if not user_clean:
        errors.append("Nama pengguna (username) wajib diisi.")
    elif len(user_clean) < 3:
        errors.append("Nama pengguna minimal 3 karakter.")
    elif not re.match(r"^[a-zA-Z0-9_]+$", user_clean):
        errors.append("Nama pengguna hanya boleh berisi huruf, angka, dan garis bawah (_).")

    if not pass_clean:
        errors.append("Kata sandi wajib diisi.")
    elif len(pass_clean) < 6:
        errors.append("Kata sandi minimal 6 karakter.")

    if role_clean not in ("kasir", "owner"):
        errors.append("Peran pengguna harus salah satu dari: 'kasir' atau 'owner'.")

    if errors:
        return False, errors, None

    conn = get_db_connection(db_name)
    try:
        # Cek apakah nama pengguna sudah digunakan
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?;", (user_clean,)
        ).fetchone()

        if existing:
            errors.append(f"Nama pengguna '{user_clean}' sudah digunakan. Pilih nama lain.")
            return False, errors, None

        # Hash kata sandi dengan salt aman otomatis (scrypt/pbkdf2:sha256)
        hashed_password = generate_password_hash(pass_clean)

        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, role, is_active) VALUES (?, ?, ?, ?);",
            (user_clean, hashed_password, role_clean, 1 if is_active else 0),
        )
        conn.commit()
        return True, [], cursor.lastrowid
    except sqlite3.IntegrityError as e:
        errors.append(f"Pelanggaran integritas basis data pengguna: {e}")
        return False, errors, None
    finally:
        conn.close()


def authenticate_user(username, password, db_name=None):
    """
    Langkah 4 (Siklus 2): Memverifikasi kredensial login pengguna.
    Menggunakan pesan galat identik untuk username salah maupun password salah
    guna menangkal serangan user enumeration.
    Mengembalikan (user_row, error_message).
    """
    user_clean = (username or "").strip().lower()
    pass_clean = password or ""
    pesan_galat_netral = "Nama pengguna atau kata sandi salah."

    if not user_clean or not pass_clean:
        return None, pesan_galat_netral

    conn = get_db_connection(db_name)
    try:
        user = conn.execute(
            "SELECT id, username, password_hash, role, is_active FROM users WHERE username = ?;",
            (user_clean,),
        ).fetchone()

        if not user:
            return None, pesan_galat_netral

        if not user["is_active"]:
            return None, "Akun pengguna ini sedang dinonaktifkan. Hubungi pemilik sistem."

        # Verifikasi hash kata sandi ber-salt
        if not check_password_hash(user["password_hash"], pass_clean):
            return None, pesan_galat_netral

        return user, None
    finally:
        conn.close()


def get_user_by_id(user_id, db_name=None):
    """
    Mengambil data pengguna berdasarkan primary key ID.
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, username, role, is_active FROM users WHERE id = ?;",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()


def get_user_by_username(username, db_name=None):
    """
    Mengambil data pengguna berdasarkan nama pengguna (username).
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, username, role, is_active FROM users WHERE username = ?;",
            (username.strip().lower(),),
        ).fetchone()
    finally:
        conn.close()


def get_all_users(db_name=None):
    """
    Mengambil daftar seluruh pengguna (tanpa menampilkan password_hash).
    """
    conn = get_db_connection(db_name)
    try:
        return conn.execute(
            "SELECT id, username, role, is_active FROM users ORDER BY id ASC;"
        ).fetchall()
    finally:
        conn.close()
