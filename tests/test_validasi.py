"""
test_validasi.py — Uji Otomatis Pytest Berbasis Spesifikasi Nilai Batas dan Partisi Ekuivalen (Langkah 5)
Menggunakan @pytest.mark.parametrize dan fixture conftest.py.
"""

import pytest
from services import (
    create_package,
    create_console,
    create_transaction,
    finish_transaction,
    get_console_by_id,
    get_transaction_by_id,
)


# ============================================================================
# 1. PENGUJIAN NILAI BATAS HARGA PAKET SEWA (KF-02, KF-08)
# ============================================================================
@pytest.mark.parametrize(
    "nama, durasi, harga, diharapkan_sukses, pesan_galat",
    [
        ("Paket Promo Gratis", 60, "0", True, None),                     # TC-BVA-01: Batas bawah harga 0
        ("Paket Minus Tidak Valid", 60, "-1", False, "tidak boleh bernilai negatif"), # TC-BVA-02: Bawah batas (-1)
        ("Paket Normal 10k", 60, "10000", True, None),                   # Jalur Normal
    ],
)
def test_validasi_nilai_batas_harga_paket(test_db_path, nama, durasi, harga, diharapkan_sukses, pesan_galat):
    """Menguji penanganan nilai batas harga paket sewa (0 vs -1)."""
    sukses, errors, pkg_id = create_package(
        nama_paket=nama,
        jenis_konsol="PS4",
        durasi_menit=durasi,
        harga=harga,
        db_name=test_db_path,
    )
    assert sukses is diharapkan_sukses
    if diharapkan_sukses:
        assert pkg_id is not None
        assert errors == []
    else:
        assert any(pesan_galat in err for err in errors)


# ============================================================================
# 2. PENGUJIAN NILAI BATAS DURASI PAKET SEWA (KF-02, KF-08)
# ============================================================================
@pytest.mark.parametrize(
    "nama, durasi, harga, diharapkan_sukses, pesan_galat",
    [
        ("Paket Nol Menit", 0, 10000, False, "lebih besar dari 0 menit"),   # TC-BVA-03: Batas invalid (0)
        ("Paket 1 Menit Batas", 1, 5000, True, None),                      # TC-BVA-04: Batas bawah valid (1)
        ("Paket Standar 120m", 120, 20000, True, None),                    # Jalur Normal
    ],
)
def test_validasi_nilai_batas_durasi_paket(test_db_path, nama, durasi, harga, diharapkan_sukses, pesan_galat):
    """Menguji penanganan nilai batas durasi paket sewa (0 menit vs 1 menit)."""
    sukses, errors, pkg_id = create_package(
        nama_paket=nama,
        jenis_konsol="PS5",
        durasi_menit=durasi,
        harga=harga,
        db_name=test_db_path,
    )
    assert sukses is diharapkan_sukses
    if diharapkan_sukses:
        assert pkg_id is not None
        assert errors == []
    else:
        assert any(pesan_galat in err for err in errors)


# ============================================================================
# 3. PENGUJIAN NILAI BATAS KODE UNIT KONSOL (KF-01, KF-08)
# ============================================================================
@pytest.mark.parametrize(
    "kode, jenis, diharapkan_sukses, pesan_galat",
    [
        ("PS4", "PS4", False, "minimal 4 karakter"),                        # TC-BVA-07: Batas atas invalid (3 char)
        ("PS41", "PS4", True, None),                                        # TC-BVA-08: Batas bawah valid (4 char)
        ("", "PS4", False, "wajib diisi"),                                  # TC-NEG-01: Kode kosong
        ("XB-01", "XBOX", False, "Jenis konsol tidak valid"),                # TC-NEG-02: Jenis dilarang
    ],
)
def test_validasi_nilai_batas_kode_konsol(test_db_path, kode, jenis, diharapkan_sukses, pesan_galat):
    """Menguji validasi panjang kode konsol dan jenis konsol."""
    sukses, errors, console_id = create_console(
        kode_konsol=kode,
        jenis_konsol=jenis,
        db_name=test_db_path,
    )
    assert sukses is diharapkan_sukses
    if diharapkan_sukses:
        assert console_id is not None
        assert errors == []
    else:
        assert any(pesan_galat in err for err in errors)


# ============================================================================
# 4. PENGUJIAN PELANGGARAN DUPLIKASI KONSOL & ATOMISITAS BUKA SEWA (KF-01, KF-08)
# ============================================================================
def test_duplikasi_kode_konsol_ditolak(test_db_path):
    """TC-NEG-03: Menolak penambahan kode konsol yang sudah ada di basis data."""
    create_console("PS4-DUP", "PS4", db_name=test_db_path)
    sukses, errors, _ = create_console("PS4-DUP", "PS4", db_name=test_db_path)
    assert sukses is False
    assert any("sudah terdaftar" in err for err in errors)


def test_buka_sewa_pelanggaran_input(test_db_path):
    """TC-NEG-04 & TC-NEG-06: Menolak buka sewa jika unit kosong atau nama kosong."""
    # Buka sewa konsol kosong
    ok1, err1, _ = create_transaction(nama_pelanggan="Rian", console_id="", package_id=1, db_name=test_db_path)
    assert ok1 is False
    assert any("Pilih unit konsol yang valid dari daftar" in e for e in err1)

    # Buka sewa nama pelanggan kosong
    ok2, err2, _ = create_transaction(nama_pelanggan="", console_id=1, package_id=1, db_name=test_db_path)
    assert ok2 is False
    assert any("Nama pelanggan wajib diisi" in e for e in err2)


def test_buka_sewa_konsol_sedang_terpakai_ditolak(test_db_path):
    """TC-NEG-05: Menolak penyewaan konsol yang statusnya sudah 'terpakai'."""
    _, _, c_id = create_console("PS5-BUSY", "PS5", db_name=test_db_path)
    _, _, p_id = create_package("Paket Busy Test", "PS5", 60, 15000, db_name=test_db_path)

    # Sewa pertama berhasil
    ok_first, _, tx_id = create_transaction(nama_pelanggan="Pelanggan Pertama", console_id=c_id, package_id=p_id, db_name=test_db_path)
    assert ok_first is True

    # Verifikasi status konsol menjadi terpakai
    c_data = get_console_by_id(c_id, db_name=test_db_path)
    assert c_data["status"] == "terpakai"

    # Sewa kedua pada konsol yang sama harus ditolak
    ok_second, err_second, _ = create_transaction(nama_pelanggan="Pelanggan Kedua", console_id=c_id, package_id=p_id, db_name=test_db_path)
    assert ok_second is False
    assert any("sedang tidak tersedia" in e for e in err_second)
