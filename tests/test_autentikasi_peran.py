"""
test_autentikasi_peran.py — Pengujian Menyeluruh Autentikasi & Otorisasi RBAC (Jobsheet 11)
Memverifikasi:
- Siklus 1: Hashing kata sandi ber-salt
- Siklus 2: 5 Skenario Login, Logout, dan Pencegahan Open Redirect
- Siklus 3: 4 Skenario Pembatasan Hak Akses Berdasarkan Peran (Kasir vs Owner)
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db
from services import create_user

TEST_DB = "test_auth.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

init_db(TEST_DB)
app.config["DATABASE_NAME"] = TEST_DB
app.config["TESTING"] = True
client = app.test_client()

print("--- MENJALANKAN PENGUJIAN AUTENTIKASI DAN PERAN (JOBSHEET 11) ---")

# ============================================================================
# SIKLUS 1: PEMBUATAN AKUN & VERIFIKASI HASH BER-SALT
# ============================================================================
ok_owner, _, owner_id = create_user("owner_budi", "pemilik_rahasia123", "owner", db_name=TEST_DB)
assert ok_owner is True

ok_kasir, _, kasir_id = create_user("kasir_siti", "kasir_rahasia123", "kasir", db_name=TEST_DB)
assert ok_kasir is True

# Verifikasi hash di SQLite
conn = sqlite3.connect(TEST_DB)
rows = conn.execute("SELECT username, password_hash FROM users;").fetchall()
conn.close()

assert len(rows) == 2
for username, p_hash in rows:
    assert p_hash.startswith("scrypt:") or p_hash.startswith("pbkdf2:")
    assert "pemilik_rahasia123" not in p_hash
    assert "kasir_rahasia123" not in p_hash

print("[LULUS] Siklus 1: Akun awal tersimpan dengan hash ber-salt modern.")

# ============================================================================
# SIKLUS 2: 5 PENGUJIAN LOGIN & LOGOUT (LANGKAH 4)
# ============================================================================

# Uji 1: Kata sandi benar -> Masuk dan dialihkan ke halaman utama / daftar sewa
res_l1 = client.post(
    "/login",
    data={"username": "kasir_siti", "password": "kasir_rahasia123"},
    follow_redirects=True,
)
assert res_l1.status_code == 200
assert "Selamat datang kembali, kasir_siti" in res_l1.text
print("[LULUS] Uji 1: Kata sandi benar -> Sukses masuk ke sistem.")

# Logout terlebih dahulu
res_out = client.post("/logout", follow_redirects=True)
assert res_out.status_code == 200
assert "Anda telah keluar dari sistem" in res_out.text

# Uji 2: Kata sandi salah -> Pesan netral
res_l2 = client.post(
    "/login",
    data={"username": "kasir_siti", "password": "passwordsalah123"},
)
assert res_l2.status_code == 200
assert "Nama pengguna atau kata sandi salah" in res_l2.text
print("[LULUS] Uji 2: Kata sandi salah -> Pesan galat netral ditampilkan.")

# Uji 3: Nama pengguna tidak ada -> Pesan yang sama persis dengan uji 2
res_l3 = client.post(
    "/login",
    data={"username": "user_tidak_ada", "password": "bebaspassword"},
)
assert res_l3.status_code == 200
assert "Nama pengguna atau kata sandi salah" in res_l3.text
print("[LULUS] Uji 3: Nama pengguna tidak ada -> Pesan galat identik (anti user enumeration).")

# Uji 4: Open Redirect Protection (/login?next=https://jahat.example)
res_l4 = client.post(
    "/login?next=https://jahat.example",
    data={"username": "kasir_siti", "password": "kasir_rahasia123"},
)
# Harus dialihkan ke rute internal /sewa, BUKAN ke https://jahat.example
assert res_l4.status_code == 302
assert "jahat.example" not in res_l4.location
assert res_l4.location == "/sewa"
print("[LULUS] Uji 4: Open redirect (https://jahat.example) berhasil dicegah dan dinetralkan.")

# Uji 5: Tekan Keluar, lalu buka halaman daftar -> Dialihkan ke login
client.post("/logout")
res_l5 = client.get("/sewa")
assert res_l5.status_code == 302
assert "/login" in res_l5.location
print("[LULUS] Uji 5: Setelah keluar, akses rute terproteksi dialihkan ke login.")

# ============================================================================
# SIKLUS 3: 4 PENGUJIAN PEMBATASAN AKSES BERDASARKAN PERAN (LANGKAH 5)
# ============================================================================

# Skenario 1: Tamu membuka alamat halaman utama -> Dialihkan ke login
client.post("/logout")
res_s1 = client.get("/consoles")
assert res_s1.status_code == 302
assert "/login?next=/consoles" in res_s1.location
print("[LULUS] Skenario 1: Tamu membuka rute master dialihkan ke login.")

# Skenario 2: Peran terbatas (kasir) membuka alamat tambah data -> 403 Forbidden
# Login sebagai kasir
client.post("/login", data={"username": "kasir_siti", "password": "kasir_rahasia123"})
res_s2 = client.get("/consoles/tambah")
assert res_s2.status_code == 403
assert "403 — Akses Ditolak" in res_s2.text
print("[LULUS] Skenario 2: Kasir mencoba membuka halaman tambah konsol ditolak (403).")

# Skenario 3: Peran terbatas (kasir) mengirim POST hapus / ubah -> 403 Forbidden dan data tidak berubah
# Buat data konsol awal
conn = sqlite3.connect(TEST_DB)
conn.execute("INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (10, 'PS4-TEST', 'PS4', 'tersedia');")
conn.commit()
conn.close()

res_s3 = client.post("/consoles/10/hapus")
assert res_s3.status_code == 403
assert "403 — Akses Ditolak" in res_s3.text

# Buktikan data konsol 10 tetap ada di database (tidak terhapus)
conn = sqlite3.connect(TEST_DB)
row_c = conn.execute("SELECT id FROM consoles WHERE id = 10;").fetchone()
conn.close()
assert row_c is not None
print("[LULUS] Skenario 3: Kasir mengirim POST hapus terblokir 403; data tetap utuh.")

# Skenario 4: Peran penuh (owner) membuka alamat yang sama -> Berhasil
# Logout lalu login sebagai owner
client.post("/logout")
client.post("/login", data={"username": "owner_budi", "password": "pemilik_rahasia123"})

# Buka form tambah konsol
res_s4_get = client.get("/consoles/tambah")
assert res_s4_get.status_code == 200
assert "Tambah Unit Konsol" in res_s4_get.text

# Hapus konsol 10
res_s4_post = client.post("/consoles/10/hapus", follow_redirects=True)
assert res_s4_post.status_code == 200
assert "berhasil dihapus" in res_s4_post.text

# Buktikan data konsol 10 sudah terhapus oleh owner
conn = sqlite3.connect(TEST_DB)
row_c2 = conn.execute("SELECT id FROM consoles WHERE id = 10;").fetchone()
conn.close()
assert row_c2 is None
print("[LULUS] Skenario 4: Owner membuka form dan mengeksekusi aksi berhasil 100%.")

print("\n--- SELURUH PENGUJIAN AUTENTIKASI DAN PERAN LULUS 100% ---")

if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
