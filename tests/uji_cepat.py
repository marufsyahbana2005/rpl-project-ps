"""
uji_cepat.py — Skrip Uji Regresi Otomatis Mandiri (Langkah 12)
Menguji seluruh alur CRUD konsol, paket, relasi transaksi sewa atomik,
pencarian, dan penegakan kunci asing menggunakan basis data sementara (temp_uji.db),
tanpa menyentuh basis data utama produksi (rental.db).
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db

TEMP_DB = "temp_uji.db"
if os.path.exists(TEMP_DB):
    os.remove(TEMP_DB)

# Inisialisasi skema basis data sementara
init_db(TEMP_DB)
app.config["DATABASE_NAME"] = TEMP_DB
app.config["TESTING"] = True
client = app.test_client()

# Data Awal
conn = sqlite3.connect(TEMP_DB)
conn.execute("INSERT INTO users (id, username, password_hash, role) VALUES (1, 'kasir1', 'hash', 'kasir');")
conn.execute("INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (1, 'PS4-REG', 'PS4', 'tersedia');")
conn.execute("INSERT INTO packages (id, nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (1, 'Paket 1 Jam', 'PS4', 60, 10000, 1);")
conn.commit()
conn.close()

# 1. Uji Daftar Konsol
r = client.get("/consoles")
assert r.status_code == 200
assert "PS4-REG" in r.text

# 2. Uji Tambah Konsol Valid
r = client.post("/consoles/tambah", data={"kode_konsol": "PS5-REG", "jenis_konsol": "PS5"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-REG" in r.text

# 3. Uji Tambah Konsol Tidak Valid (Kode kosong)
r = client.post("/consoles/tambah", data={"kode_konsol": "", "jenis_konsol": "PS5"})
assert r.status_code == 200
assert "Kode konsol wajib diisi" in r.text

# 4. Uji Ubah Konsol
r = client.post("/consoles/2/ubah", data={"kode_konsol": "PS5-EDIT", "jenis_konsol": "PS5", "status": "maintenance"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-EDIT" in r.text

# 5. Uji Hapus Konsol Bebas Transaksi
r = client.post("/consoles/2/hapus", follow_redirects=True)
assert r.status_code == 200
assert "berhasil dihapus" in r.text

# 6. Uji Daftar Transaksi dengan JOIN
r = client.get("/sewa")
assert r.status_code == 200

# 7. Uji Transaksi Atomik Sewa Konsol (Dua tabel berubah bersama)
r = client.post("/sewa/buka", data={"nama_pelanggan": "Dewi Sartika", "console_id": "1", "package_id": "1", "status_bayar": "open_bill"}, follow_redirects=True)
assert r.status_code == 200
assert "Dewi Sartika" in r.text
assert "PS4-REG" in r.text

# Buktikan status unit PS4-REG berubah jadi 'terpakai' di database
conn = sqlite3.connect(TEMP_DB)
c_status = conn.execute("SELECT status FROM consoles WHERE id = 1;").fetchone()[0]
conn.close()
assert c_status == "terpakai"

# 8. Uji Tambah Sewa Tidak Valid (ID Konsol 999 tidak ada)
r = client.post("/sewa/buka", data={"nama_pelanggan": "Salah ID", "console_id": "999", "package_id": "1"})
assert r.status_code == 200
assert "tidak ditemukan di sistem" in r.text

# 9. Uji Pencarian LIKE Berparameter
r = client.get("/sewa?q=Dewi")
assert r.status_code == 200
assert "Dewi Sartika" in r.text

# 10. Uji Proteksi Foreign Key (Konsol berelasi tidak dapat dihapus)
r = client.post("/consoles/1/hapus", follow_redirects=True)
assert r.status_code == 200
assert "tidak dapat dihapus karena memiliki" in r.text

# 11. Uji Penghentian Sesi Sewa & Kembalinya Status Unit Konsol (Langkah 16)
r = client.post("/sewa/1/selesai", follow_redirects=True)
assert r.status_code == 200
assert "berhasil diselesaikan" in r.text

conn = sqlite3.connect(TEMP_DB)
c_status = conn.execute("SELECT status FROM consoles WHERE id = 1;").fetchone()[0]
conn.close()
assert c_status == "tersedia"

# Bersihkan database sementara
if os.path.exists(TEMP_DB):
    os.remove(TEMP_DB)

print("SEMUA UJI LULUS")
