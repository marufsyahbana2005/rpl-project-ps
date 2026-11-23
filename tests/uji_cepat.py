"""
uji_cepat.py — Skrip Uji Regresi Otomatis Mandiri (Langkah 12 / Jobsheet 11)
Menguji:
1. Autentikasi dan Otorisasi Berbasis Peran (RBAC - Kasir vs Owner):
   - Tamu dialihkan ke login.
   - Kata sandi salah vs nama pengguna tidak ada menghasilkan pesan galat identik.
   - Open redirect (https://jahat.example) diabaikan/dinormalkan.
   - Kata sandi tersimpan sebagai hash ber-salt (scrypt/pbkdf2).
   - Peran terbatas (kasir) terblokir 403 pada rute master dan POST terlarang.
   - Peran penuh (owner) berhasil masuk dan mengeksekusi aksi.
2. Alur lengkap CRUD konsol, paket, transaksi sewa atomik multi-tabel,
   pencarian berparameter, penegakan FK, dan penghentian sewa dengan denda.
Menggunakan basis data terisolasi (temp_uji.db) tanpa menyentuh rental.db.
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db
from services import create_user

TEMP_DB = "temp_uji.db"
if os.path.exists(TEMP_DB):
    os.remove(TEMP_DB)

# Inisialisasi basis data sementara
init_db(TEMP_DB)
app.config["DATABASE_NAME"] = TEMP_DB
app.config["TESTING"] = True
client = app.test_client()

# ============================================================================
# 1. PERSIAPAN PENGGUNA BER-HASH (LANGKAH 3)
# ============================================================================
ok_owner, _, owner_id = create_user("owner_budi", "pemilik_aman123", "owner", db_name=TEMP_DB)
assert ok_owner is True

ok_kasir, _, kasir_id = create_user("kasir_siti", "kasir_aman123", "kasir", db_name=TEMP_DB)
assert ok_kasir is True

# Data Awal Konsol & Paket
conn = sqlite3.connect(TEMP_DB)
conn.execute("INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (1, 'PS4-REG', 'PS4', 'tersedia');")
conn.execute("INSERT INTO packages (id, nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (1, 'Paket 1 Jam', 'PS4', 60, 10000, 1);")
conn.commit()
conn.close()

# ============================================================================
# 2. ENAM UJI AUTENTIKASI & PERAN (LANGKAH 12 / JOBSHEET 11)
# ============================================================================

# Uji A1: Tamu diarahkan ke login
r_tamu = client.get("/consoles")
assert r_tamu.status_code == 302
assert "/login?next=/consoles" in r_tamu.location

# Uji A2: Kata sandi salah dan nama pengguna salah menghasilkan pesan sama persis
r_pass_salah = client.post("/login", data={"username": "kasir_siti", "password": "passwordsalah"})
assert r_pass_salah.status_code == 200
assert "Nama pengguna atau kata sandi salah" in r_pass_salah.text

r_user_salah = client.post("/login", data={"username": "user_gaib", "password": "passwordsalah"})
assert r_user_salah.status_code == 200
assert "Nama pengguna atau kata sandi salah" in r_user_salah.text

# Uji A3: Open redirect (https://jahat.example) diabaikan dan dialihkan ke internal /sewa
r_open_redir = client.post(
    "/login?next=https://jahat.example",
    data={"username": "kasir_siti", "password": "kasir_aman123"},
)
assert r_open_redir.status_code == 302
assert "jahat.example" not in r_open_redir.location
assert r_open_redir.location == "/sewa"

# Uji A4: Kata sandi tersimpan sebagai hash ber-salt di database (bukan plaintext)
conn = sqlite3.connect(TEMP_DB)
h_rows = conn.execute("SELECT password_hash FROM users;").fetchall()
conn.close()
for (h,) in h_rows:
    assert h.startswith("scrypt:") or h.startswith("pbkdf2:")
    assert "kasir_aman123" not in h
    assert "pemilik_aman123" not in h

# Uji A5: Peran terbatas (kasir) mendapat 403 pada rute master dan POST terlarang
# Saat ini kasir_siti sedang login
r_kasir_master = client.get("/packages")
assert r_kasir_master.status_code == 403
assert "403 — Akses Ditolak" in r_kasir_master.text

r_kasir_post = client.post("/consoles/1/hapus")
assert r_kasir_post.status_code == 403

# Logout kasir
client.post("/logout")

# Uji A6: Peran penuh (owner) berhasil masuk dan mengeksekusi operasi master
r_owner_login = client.post(
    "/login",
    data={"username": "owner_budi", "password": "pemilik_aman123"},
    follow_redirects=True,
)
assert r_owner_login.status_code == 200
assert "Selamat datang kembali, owner_budi" in r_owner_login.text

# ============================================================================
# 3. UJI REGRESI FITUR MASTER & TRANSAKSI (SESI LOGIN OWNER)
# ============================================================================

# 1. Uji Daftar Konsol
r = client.get("/consoles")
assert r.status_code == 200
assert "PS4-REG" in r.text

# 2. Uji Tambah Konsol Valid (Owner)
r = client.post("/consoles/tambah", data={"kode_konsol": "PS5-REG", "jenis_konsol": "PS5"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-REG" in r.text

# 3. Uji Tambah Konsol Tidak Valid (Kode kosong)
r = client.post("/consoles/tambah", data={"kode_konsol": "", "jenis_konsol": "PS5"})
assert r.status_code == 200
assert "Kode konsol wajib diisi" in r.text

# 4. Uji Ubah Konsol (Owner)
r = client.post("/consoles/2/ubah", data={"kode_konsol": "PS5-EDIT", "jenis_konsol": "PS5", "status": "maintenance"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-EDIT" in r.text

# 5. Uji Hapus Konsol Bebas Transaksi (Owner)
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

# 11. Uji Penghentian Sesi Sewa & Kembalinya Status Unit Konsol
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
