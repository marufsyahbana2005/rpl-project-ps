"""
test_pertama.py — Uji Pertama pytest (Langkah 2)
Menguji bahwa penambahan paket dengan harga "0" (paket gratis/promosi) valid tanpa galat.
"""

from services import create_package


def test_tambah_paket_harga_nol_valid(test_db_path):
    """Memverifikasi bahwa harga sewa '0' (promosi) diperbolehkan dan tidak memicu galat."""
    sukses, errors, pkg_id = create_package(
        nama_paket="Paket Promosi Uji Nol",
        jenis_konsol="PS4",
        durasi_menit=60,
        harga="0",
        db_name=test_db_path
    )
    assert sukses is True
    assert errors == []
    assert pkg_id is not None
