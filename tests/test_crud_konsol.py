"""
test_crud_konsol.py — Pengujian Komprehensif Siklus 4 & 5 (Ubah, Hapus, Keamanan)
Memverifikasi:
- F4: Ubah data, tolak duplikat, dan 404 pada ID invalid.
- F5: Hapus via POST, proteksi foreign key, dan tolak GET.
- Keamanan: Uji SQL Injection dan Uji XSS Jinja2 autoescape.
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db

TEST_DB = "test_crud.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

init_db(TEST_DB)
app.config["DATABASE_NAME"] = TEST_DB
client = app.test_client()

# Seed 1 data awal
conn = sqlite3.connect(TEST_DB)
conn.execute(
    "INSERT INTO consoles (kode_konsol, jenis_konsol, status) VALUES ('PS4-ORIG', 'PS4', 'tersedia');"
)
conn.execute(
    "INSERT INTO consoles (kode_konsol, jenis_konsol, status) VALUES ('PS5-DUPL', 'PS5', 'tersedia');"
)
conn.commit()
conn.close()

print("--- MENJALANKAN PENGUJIAN SIKLUS 4 & 5 ---")

# 1. UJI F4: Ubah data berhasil
res_ubah = client.post(
    "/consoles/1/ubah",
    data={"kode_konsol": "PS4-EDITED", "jenis_konsol": "PS4", "status": "maintenance"},
    follow_redirects=True,
)
assert res_ubah.status_code == 200
assert "PS4-EDITED" in res_ubah.text
assert "berhasil diperbarui" in res_ubah.text
print("[LULUS] F4-1: Ubah data berhasil -> Tersimpan dan muncul flash sukses.")

# 2. UJI F4: Ubah menjadi kode yang sudah ada (duplikat) ditolak
res_dupl = client.post(
    "/consoles/1/ubah",
    data={"kode_konsol": "PS5-DUPL", "jenis_konsol": "PS4", "status": "tersedia"},
)
assert res_dupl.status_code == 400
assert "sudah digunakan oleh unit lain" in res_dupl.text
print("[LULUS] F4-2: Ubah ke kode duplikat ditolak dengan status 400.")

# 3. UJI F4: ID tidak ada menghasilkan respons 404
res_404 = client.get("/consoles/999/ubah")
assert res_404.status_code == 404
assert "tidak ditemukan" in res_404.text
print("[LULUS] F4-3: Akses /consoles/999/ubah mengembalikan 404 Not Found.")

# 4. UJI F5: Hapus via POST untuk unit yang belum dipakai transaksi
res_hapus = client.post("/consoles/2/hapus", follow_redirects=True)
assert res_hapus.status_code == 200
assert "berhasil dihapus" in res_hapus.text
print("[LULUS] F5-1: Hapus via POST berhasil untuk data bebas transaksi.")

# 5. UJI F5: Coba hapus via GET -> Tidak menghapus (Method Not Allowed 405)
res_get_hapus = client.get("/consoles/1/hapus")
assert res_get_hapus.status_code == 405
print("[LULUS] F5-2: Akses GET ke rute hapus ditolak (HTTP 405 Method Not Allowed).")

# 6. UJI F5: Proteksi Foreign Key (Unit konsol yang punya transaksi ditolak dihapus)
conn = sqlite3.connect(TEST_DB)
conn.execute(
    "INSERT INTO users (username, password_hash, role) VALUES ('kasir1', 'hash', 'kasir');"
)
conn.execute(
    "INSERT INTO packages (nama_paket, jenis_konsol, durasi_menit, harga) VALUES ('P1', 'PS4', 60, 10000);"
)
conn.execute(
    "INSERT INTO transactions (nama_pelanggan, user_id, console_id, package_id, waktu_mulai) VALUES ('Budi', 1, 1, 1, '2026-11-16 10:00:00');"
)
conn.commit()
conn.close()

res_hapus_fk = client.post("/consoles/1/hapus", follow_redirects=True)
assert res_hapus_fk.status_code == 200
assert "tidak dapat dihapus karena memiliki 1 riwayat transaksi" in res_hapus_fk.text
print("[LULUS] F5-3: Proteksi Foreign Key berhasil -> Penghapusan ditolak ramah tanpa crash.")

# 7. UJI KEAMANAN 1: SQL Injection (Robert'); DROP TABLE consoles;--)
res_sqli = client.post(
    "/consoles/tambah",
    data={"kode_konsol": "Robert'); DROP TABLE consoles;--", "jenis_konsol": "PS4"},
    follow_redirects=True,
)
assert res_sqli.status_code == 200
# Verifikasi tabel consoles MASIH ADA dan data tersimpan sebagai teks biasa
conn = sqlite3.connect(TEST_DB)
check_table = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='consoles';"
).fetchone()
assert check_table is not None
saved_text = conn.execute(
    "SELECT kode_konsol FROM consoles WHERE kode_konsol LIKE 'ROBERT%';"
).fetchone()
assert saved_text is not None
conn.close()
print("[LULUS] Keamanan 1: SQL Injection dicegah oleh SQL berparameter. Tabel tetap utuh.")

# 8. UJI KEAMANAN 2: XSS Escape Otomatis Jinja2 (<b>tes</b>)
res_xss = client.post(
    "/consoles/tambah",
    data={"kode_konsol": "<b>TEST-XSS</b>", "jenis_konsol": "PS5"},
    follow_redirects=True,
)
assert res_xss.status_code == 200
assert "&lt;B&gt;TEST-XSS&lt;/B&gt;" in res_xss.text
assert "<b>TEST-XSS</b>" not in res_xss.text
print("[LULUS] Keamanan 2: XSS dicegah otomatis oleh Jinja2 auto-escaping.")

print("--- SELURUH PENGUJIAN SIKLUS 4, 5, DAN KEAMANAN LULUS 100% ---")

if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
