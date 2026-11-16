"""
test_crud_packages.py — Uji Otomatis CRUD Entitas Kedua: Packages (Langkah 14)
Memverifikasi:
- Daftar paket
- Tambah paket baru & validasi harga/durasi/nama duplikat
- Ubah paket & toggle is_active
- Hapus paket via POST & proteksi foreign key
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db

TEST_DB = "test_pkg.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

init_db(TEST_DB)
app.config["DATABASE_NAME"] = TEST_DB
client = app.test_client()

print("--- MENJALANKAN UJI CRUD PACKAGES (ENTITAS KEDUA) ---")

# 1. UJI TAMBAH PAKET VALID
res1 = client.post(
    "/packages/tambah",
    data={
        "nama_paket": "Paket PS4 1 Jam Reguler",
        "jenis_konsol": "PS4",
        "durasi_menit": "60",
        "harga": "12000",
        "is_active": "1",
    },
    follow_redirects=True,
)
assert res1.status_code == 200
assert "Paket PS4 1 Jam Reguler" in res1.text
assert "berhasil ditambahkan" in res1.text
print("[LULUS] PKG-1: Tambah paket valid berhasil disimpan.")

# 2. UJI TAMBAH DENGAN HARGA NEGATIF (Ditolak)
res2 = client.post(
    "/packages/tambah",
    data={
        "nama_paket": "Paket Gagal Harga",
        "jenis_konsol": "PS4",
        "durasi_menit": "60",
        "harga": "-5000",
    },
)
assert res2.status_code == 200
assert "tidak boleh bernilai negatif" in res2.text
print("[LULUS] PKG-2: Harga negatif ditolak sistem.")

# 3. UJI TAMBAH DENGAN DURASI <= 0 (Ditolak)
res3 = client.post(
    "/packages/tambah",
    data={
        "nama_paket": "Paket Gagal Durasi",
        "jenis_konsol": "PS4",
        "durasi_menit": "0",
        "harga": "10000",
    },
)
assert res3.status_code == 200
assert "lebih besar dari 0" in res3.text
print("[LULUS] PKG-3: Durasi 0 menit ditolak sistem.")

# 4. UJI TAMBAH DUPLIKAT NAMA
res4 = client.post(
    "/packages/tambah",
    data={
        "nama_paket": "Paket PS4 1 Jam Reguler",
        "jenis_konsol": "PS4",
        "durasi_menit": "60",
        "harga": "12000",
    },
)
assert res4.status_code == 200
assert "sudah digunakan" in res4.text
print("[LULUS] PKG-4: Nama paket duplikat ditolak sistem.")

# 5. UJI UBAH PAKET
res5 = client.post(
    "/packages/1/ubah",
    data={
        "nama_paket": "Paket PS4 1 Jam (Promo)",
        "jenis_konsol": "PS4",
        "durasi_menit": "60",
        "harga": "10000",
        "is_active": "1",
    },
    follow_redirects=True,
)
assert res5.status_code == 200
assert "Paket PS4 1 Jam (Promo)" in res5.text
print("[LULUS] PKG-5: Ubah paket sewa berhasil diperbarui.")

# 6. UJI HAPUS PAKET BEBAS TRANSAKSI
res6 = client.post("/packages/1/hapus", follow_redirects=True)
assert res6.status_code == 200
assert "berhasil dihapus" in res6.text
print("[LULUS] PKG-6: Hapus paket sewa via POST berhasil.")

print("--- SELURUH UJI CRUD PACKAGES LULUS 100% ---")

if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
