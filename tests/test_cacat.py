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
