"""
test_tambah_konsol.py — Uji Otomatis Form Tambah Konsol (Langkah 6)
Menguji 5 variasi masukan: valid, kosong, pendek, jenis invalid, dan duplikat.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import init_db

init_db("test_rental.db")
app.config["DATABASE_NAME"] = "test_rental.db"
client = app.test_client()

# Inisialisasi sesi login peran owner (Langkah 12)
with client.session_transaction() as sess:
    sess["user_id"] = 1
    sess["username"] = "owner_test"
    sess["role"] = "owner"

print("--- MENJALANKAN 5 PENGUJIAN FORM TAMBAH KONSOL ---")

# Uji 1: Semua kolom valid
res1 = client.post(
    "/consoles/tambah",
    data={"kode_konsol": "PS4-99", "jenis_konsol": "PS4"},
    follow_redirects=True,
)
assert res1.status_code == 200
assert "PS4-99" in res1.text
assert "berhasil ditambahkan" in res1.text
print("[LULUS] Uji 1: Semua kolom valid -> Tersimpan dan muncul pesan sukses.")

# Uji 2: Kode kosong
res2 = client.post(
    "/consoles/tambah", data={"kode_konsol": "", "jenis_konsol": "PS4"}
)
assert res2.status_code == 200
assert "Kode konsol wajib diisi" in res2.text
print("[LULUS] Uji 2: Kode kosong -> Ditolak dengan pesan galat.")

# Uji 3: Kode terlalu pendek (< 4 karakter)
res3 = client.post(
    "/consoles/tambah", data={"kode_konsol": "PS", "jenis_konsol": "PS4"}
)
assert res3.status_code == 200
assert "minimal 4 karakter" in res3.text
print(
    "[LULUS] Uji 3: Kode terlalu pendek -> Ditolak dengan batas minimal"
    " karakter."
)

# Uji 4: Jenis konsol tidak valid
res4 = client.post(
    "/consoles/tambah", data={"kode_konsol": "XB-01", "jenis_konsol": "NINTENDO"}
)
assert res4.status_code == 200
assert "Jenis konsol tidak valid" in res4.text
print("[LULUS] Uji 4: Jenis konsol tidak valid -> Ditolak.")

# Uji 5: Kode konsol duplikat (sudah ada)
res5 = client.post(
    "/consoles/tambah",
    data={"kode_konsol": "PS4-99", "jenis_konsol": "PS4"},
)
assert res5.status_code == 200
assert "sudah terdaftar" in res5.text
print(
    "[LULUS] Uji 5: Kode konsol sudah ada -> Ditolak dengan pesan sudah"
    " terdaftar."
)

print("--- SEMUA 5 UJI FORM TAMBAH KONSOL LULUS 100% ---")
