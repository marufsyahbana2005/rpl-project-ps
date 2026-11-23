"""
test_cacat.py — Uji Regresi Perbaikan Cacat D-01, D-02, dan D-03 (Langkah 11)
Mengikuti siklus TDD Merah -> Hijau.
"""

import pytest
from services import (
    create_transaction,
    create_package,
    create_console,
    update_console,
    get_console_by_id,
)


# ============================================================================
# CACAT 1: D-01 — Penanganan Tipe Masukan Non-String pada nama_pelanggan
# ============================================================================
def test_cacat_d01_nama_pelanggan_non_string_handled_safely(test_db_path):
    """
    D-01: Memverifikasi bahwa masukan nama_pelanggan non-string (misal integer 12345)
    dikonversi secara aman tanpa memicu AttributeError (HTTP 500).
    """
    # Siapkan unit konsol dan paket sewa
    _, _, c_id = create_console("PS4-D01", "PS4", db_name=test_db_path)
    _, _, p_id = create_package("Paket D01", "PS4", 60, 10000, db_name=test_db_path)

    # Masukan berupa integer angka (12345)
    sukses, errors, tx_id = create_transaction(
        nama_pelanggan=12345,
        console_id=c_id,
        package_id=p_id,
        db_name=test_db_path,
    )
    # Harus ditangani dengan aman: berhasil disimpan sebagai string "12345"
    assert sukses is True
    assert tx_id is not None
    assert errors == []


# ============================================================================
# CACAT 2: D-02 — Duplikasi Nama Paket Sewa Berbeda Huruf Besar-Kecil
# ============================================================================
def test_cacat_d02_duplikasi_nama_paket_case_insensitive(test_db_path):
    """
    D-02: Memverifikasi bahwa pendaftaran nama paket dengan perbedaan huruf besar-kecil
    ('Paket Malam' vs 'paket malam') ditolak sebagai duplikat.
    """
    ok1, _, p1_id = create_package("Paket Malam", "PS4", 120, 20000, db_name=test_db_path)
    assert ok1 is True

    # Pendaftaran kedua dengan huruf kecil seluruhnya
    ok2, errors2, _ = create_package("paket malam", "PS4", 120, 20000, db_name=test_db_path)
    assert ok2 is False
    assert any("sudah digunakan" in err for err in errors2)


# ============================================================================
# CACAT 3: D-03 — Larangan Mengubah Status Konsol yang Sedang Disewa Aktif
# ============================================================================
def test_cacat_d03_ubah_status_konsol_terpakai_ditolak(test_db_path):
    """
    D-03: Memverifikasi bahwa unit konsol yang sedang disewa aktif ('terpakai')
    tidak dapat diubah statusnya secara manual menjadi 'maintenance' atau 'tersedia'.
    """
    _, _, c_id = create_console("PS4-LOCK", "PS4", db_name=test_db_path)
    _, _, p_id = create_package("Paket Lock", "PS4", 60, 10000, db_name=test_db_path)

    # Buka sewa aktif
    ok_tx, _, _ = create_transaction("Pelanggan Kunci", c_id, p_id, db_name=test_db_path)
    assert ok_tx is True
    assert get_console_by_id(c_id, db_name=test_db_path)["status"] == "terpakai"

    # Pemilik mencoba mengubah status menjadi maintenance
    sukses_ubah, errors_ubah, code = update_console(
        console_id=c_id,
        kode_konsol="PS4-LOCK",
        jenis_konsol="PS4",
        status="maintenance",
        db_name=test_db_path,
    )
    # Wajib ditolak
    assert sukses_ubah is False
    assert code == 400
    assert any("sedang dalam sesi sewa aktif" in err for err in errors_ubah)
