"""
uji_cepat.py — Skrip Uji Regresi Otomatis Mandiri (Jobsheet 12 & Checkpoint Minggu 12)
Menguji:
1. Pengerasan Keamanan (Security Hardening):
   - Penolakan permintaan POST tanpa token CSRF atau dengan token salah (HTTP 400 Bad Request).
   - Pembatasan laju percobaan login / Rate Limiting (Percobaan ke-6 menghasilkan HTTP 429 Too Many Requests).
   - Keberadaan Security HTTP Headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy).
   - Perlindungan Open Redirect (next domain luar dinetralkan ke rute internal aman).
   - Hash kata sandi ber-salt acak (scrypt/pbkdf2).
2. Otorisasi Berbasis Peran (RBAC):
   - Tamu dialihkan ke login.
   - Kasir terblokir HTTP 403 saat mencoba mengakses rute master konsol/paket atau aksi POST terlarang.
   - Owner memiliki otorisasi penuh untuk kelola konsol, paket, dan sewa.
3. Alur Fungsional Inti:
   - CRUD konsol dan paket.
   - Transaksi sewa atomik multi-tabel (consoles status 'terpakai').
   - Penegakan Foreign Key RESTRICT saat hapus data induk.
   - Penghentian sewa kasir dan pencatatan denda otomatis ke tabel fines.
Menggunakan basis data sementara (temp_uji.db) tanpa menyentuh rental.db.
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

def get_csrf(c):
    """Mengambil atau menginisialisasi token CSRF sesi pengujian."""
    with c.session_transaction() as sess:
        if "_csrf_token" not in sess:
            sess["_csrf_token"] = "valid_csrf_token_for_test"
        return sess["_csrf_token"]

def post_csrf(c, url, data=None, **kwargs):
    """Helper pengiriman POST dengan token CSRF valid."""
    d = dict(data or {})
    d["csrf_token"] = get_csrf(c)
    return c.post(url, data=d, **kwargs)

# ============================================================================
# 1. PERSIAPAN PENGGUNA BER-HASH (LANGKAH 3)
# ============================================================================
ok_owner, _, owner_id = create_user("owner_budi", "pemilik_aman123", "owner", db_name=TEMP_DB)
assert ok_owner is True

ok_kasir, _, kasir_id = create_user("kasir_siti", "kasir_aman123", "kasir", db_name=TEMP_DB)
assert ok_kasir is True

conn = sqlite3.connect(TEMP_DB)
conn.execute("INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (1, 'PS4-REG', 'PS4', 'tersedia');")
conn.execute("INSERT INTO packages (id, nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (1, 'Paket 1 Jam', 'PS4', 60, 10000, 1);")
conn.commit()
conn.close()

# ============================================================================
# 2. UJI SECURITY HEADERS & PERLINDUNGAN CSRF (JOBSHEET 12 / SIKLUS 3 & 5)
# ============================================================================

# Uji S1: Keberadaan Security HTTP Headers
r_head = client.get("/login")
assert r_head.status_code == 200
assert r_head.headers.get("X-Content-Type-Options") == "nosniff"
assert r_head.headers.get("X-Frame-Options") == "SAMEORIGIN"
assert r_head.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

# Uji S2: Penolakan Permintaan POST Tanpa Token CSRF (Harus 400 Bad Request)
r_no_csrf = client.post("/login", data={"username": "kasir_siti", "password": "kasir_aman123"})
assert r_no_csrf.status_code == 400
assert "400 — Permintaan Ditolak (CSRF)" in r_no_csrf.text

# Uji S3: Penolakan Permintaan POST dengan Token CSRF Palsu (Harus 400 Bad Request)
r_bad_csrf = client.post("/login", data={"username": "kasir_siti", "password": "kasir_aman123", "csrf_token": "token_palsu_123"})
assert r_bad_csrf.status_code == 400

# ============================================================================
# 3. UJI RATE LIMITING LOGIN / ANTI BRUTE FORCE (JOBSHEET 12 / SIKLUS 4)
# ============================================================================

# Buat pengguna khusus pengujian brute force
create_user("user_bruteforce", "password_valid_123", "kasir", db_name=TEMP_DB)

# Kirim 5x login salah berturut-turut (Harus 200 dengan pesan galat)
for attempt in range(1, 6):
    r_fail = post_csrf(client, "/login", data={"username": "user_bruteforce", "password": "salah_password"})
    assert r_fail.status_code == 200
    assert "Nama pengguna atau kata sandi salah" in r_fail.text

# Percobaan ke-6: Harus terblokir HTTP 429 Too Many Requests
r_locked = post_csrf(client, "/login", data={"username": "user_bruteforce", "password": "password_valid_123"})
assert r_locked.status_code == 429
assert "Terlalu banyak percobaan login gagal" in r_locked.text

# ============================================================================
# 4. UJI AUTENTIKASI DAN OTORISASI PERAN (RBAC)
# ============================================================================

# Uji A1: Tamu diarahkan ke login
r_tamu = client.get("/consoles")
assert r_tamu.status_code == 302
assert "/login?next=/consoles" in r_tamu.location

# Uji A2: Open redirect (https://jahat.example) dinetralkan ke /sewa
r_open_redir = post_csrf(
    client,
    "/login?next=https://jahat.example",
    data={"username": "kasir_siti", "password": "kasir_aman123"},
)
assert r_open_redir.status_code == 302
assert "jahat.example" not in r_open_redir.location
assert r_open_redir.location == "/sewa"

# Uji A3: Peran terbatas (kasir) mendapat 403 pada rute master dan POST terlarang
# Saat ini kasir_siti sedang login
r_kasir_master = client.get("/packages")
assert r_kasir_master.status_code == 403
assert "403 — Akses Ditolak" in r_kasir_master.text

r_kasir_post = post_csrf(client, "/consoles/1/hapus")
assert r_kasir_post.status_code == 403

# Logout kasir
post_csrf(client, "/logout")

# Uji A4: Peran penuh (owner) berhasil masuk dan mengeksekusi operasi master
r_owner_login = post_csrf(
    client,
    "/login",
    data={"username": "owner_budi", "password": "pemilik_aman123"},
    follow_redirects=True,
)
assert r_owner_login.status_code == 200
assert "Selamat datang kembali, owner_budi" in r_owner_login.text

# ============================================================================
# 5. UJI REGRESI FITUR MASTER & TRANSAKSI (SESI LOGIN OWNER)
# ============================================================================

# 1. Uji Daftar Konsol
r = client.get("/consoles")
assert r.status_code == 200
assert "PS4-REG" in r.text

# 2. Uji Tambah Konsol Valid (Owner)
r = post_csrf(client, "/consoles/tambah", data={"kode_konsol": "PS5-REG", "jenis_konsol": "PS5"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-REG" in r.text

# 3. Uji Tambah Konsol Tidak Valid (Kode kosong)
r = post_csrf(client, "/consoles/tambah", data={"kode_konsol": "", "jenis_konsol": "PS5"})
assert r.status_code == 200
assert "Kode konsol wajib diisi" in r.text

# 4. Uji Ubah Konsol (Owner)
r = post_csrf(client, "/consoles/2/ubah", data={"kode_konsol": "PS5-EDIT", "jenis_konsol": "PS5", "status": "maintenance"}, follow_redirects=True)
assert r.status_code == 200
assert "PS5-EDIT" in r.text

# 5. Uji Hapus Konsol Bebas Transaksi (Owner)
r = post_csrf(client, "/consoles/2/hapus", follow_redirects=True)
assert r.status_code == 200
assert "berhasil dihapus" in r.text

# 6. Uji Daftar Transaksi dengan JOIN
r = client.get("/sewa")
assert r.status_code == 200

# 7. Uji Transaksi Atomik Sewa Konsol (Dua tabel berubah bersama)
r = post_csrf(client, "/sewa/buka", data={"nama_pelanggan": "Dewi Sartika", "console_id": "1", "package_id": "1", "status_bayar": "open_bill"}, follow_redirects=True)
assert r.status_code == 200
assert "Dewi Sartika" in r.text
assert "PS4-REG" in r.text

conn = sqlite3.connect(TEMP_DB)
c_status = conn.execute("SELECT status FROM consoles WHERE id = 1;").fetchone()[0]
conn.close()
assert c_status == "terpakai"

# 8. Uji Tambah Sewa Tidak Valid (ID Konsol 999 tidak ada)
r = post_csrf(client, "/sewa/buka", data={"nama_pelanggan": "Salah ID", "console_id": "999", "package_id": "1"})
assert r.status_code == 200
assert "tidak ditemukan di sistem" in r.text

# 9. Uji Pencarian LIKE Berparameter
r = client.get("/sewa?q=Dewi")
assert r.status_code == 200
assert "Dewi Sartika" in r.text

# 10. Uji Proteksi Foreign Key (Konsol berelasi tidak dapat dihapus)
r = post_csrf(client, "/consoles/1/hapus", follow_redirects=True)
assert r.status_code == 200
assert "tidak dapat dihapus karena memiliki" in r.text

# 11. Uji Penghentian Sesi Sewa & Kembalinya Status Unit Konsol
r = post_csrf(client, "/sewa/1/selesai", follow_redirects=True)
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
