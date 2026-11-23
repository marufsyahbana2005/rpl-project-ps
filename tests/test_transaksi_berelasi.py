"""
test_transaksi_berelasi.py — Pengujian Komprehensif Modul Berelasi, Transaksi Atomik, dan FK (Jobsheet 10)
Memverifikasi:
- Langkah 4: 6 Uji masukan form buka sewa
- Langkah 5: Pembuktian atomisitas transaksi multi-tabel (transactions & consoles)
- Langkah 6: Uji penegakan Foreign Key saat hapus data induk
- Langkah 9 & 10: Uji pencarian (LIKE berparameter, escape % dan _) serta penyaringan
"""

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import init_db
from services import create_transaction, get_all_transactions

TEST_DB = "test_berelasi.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

init_db(TEST_DB)
app.config["DATABASE_NAME"] = TEST_DB
client = app.test_client()

# Inisialisasi Data Uji
conn = sqlite3.connect(TEST_DB)
conn.execute(
    "INSERT INTO users (id, username, password_hash, role) VALUES (1, 'kasir1', 'hash', 'kasir');"
)
conn.execute(
    "INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (1, 'PS4-01', 'PS4', 'tersedia');"
)
conn.execute(
    "INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (2, 'PS4-02', 'PS4', 'tersedia');"
)
conn.execute(
    "INSERT INTO consoles (id, kode_konsol, jenis_konsol, status) VALUES (3, 'PS5-BUSY', 'PS5', 'terpakai');"
)
conn.execute(
    "INSERT INTO packages (id, nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (1, 'Paket PS4 1 Jam', 'PS4', 60, 12000, 1);"
)
conn.execute(
    "INSERT INTO packages (id, nama_paket, jenis_konsol, durasi_menit, harga, is_active) VALUES (2, 'Paket Nonaktif', 'PS4', 60, 10000, 0);"
)
conn.commit()
conn.close()

print("--- MENJALANKAN PENGUJIAN MODUL BERELASI (JOBSHEET 10) ---")

# ============================================================================
# LANGKAH 4: 6 UJI FORM BUKA SEWA DENGAN PILIHAN INDUK
# ============================================================================

# Uji 1: Semua kolom valid
res1 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "Andi Saputra", "console_id": "1", "package_id": "1", "status_bayar": "open_bill"},
    follow_redirects=True,
)
assert res1.status_code == 200
assert "Andi Saputra" in res1.text
assert "berhasil dibuka" in res1.text
print("[LULUS] Uji 1: Semua kolom valid -> Transaksi tersimpan dan muncul di daftar.")

# Uji 2: Induk konsol belum dipilih
res2 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "Budi", "console_id": "", "package_id": "1"},
)
assert res2.status_code == 200
assert "Pilih unit konsol yang valid" in res2.text
print("[LULUS] Uji 2: Induk konsol kosong ditolak.")

# Uji 3: Induk paket sewa belum dipilih
res3 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "Budi", "console_id": "2", "package_id": ""},
)
assert res3.status_code == 200
assert "Pilih paket sewa yang valid" in res3.text
print("[LULUS] Uji 3: Induk paket kosong ditolak.")

# Uji 4: Nama pelanggan kosong
res4 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "", "console_id": "2", "package_id": "1"},
)
assert res4.status_code == 200
assert "Nama pelanggan wajib diisi" in res4.text
print("[LULUS] Uji 4: Nama pelanggan kosong ditolak.")

# Uji 5: Input ID bukan angka
res5 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "Budi", "console_id": "abc", "package_id": "1"},
)
assert res5.status_code == 200
assert "Pilih unit konsol yang valid" in res5.text
print("[LULUS] Uji 5: Input ID non-numerik ditolak.")

# Uji 6: ID induk 999 (tidak ada di database) dikirim manual
res6 = client.post(
    "/sewa/buka",
    data={"nama_pelanggan": "Hacker", "console_id": "999", "package_id": "1"},
)
assert res6.status_code == 200
assert "tidak ditemukan di sistem" in res6.text
print("[LULUS] Uji 6: ID induk 999 ditolak dengan pesan jelas tanpa crash.")


# ============================================================================
# LANGKAH 5: PEMBUKTIAN ATOMISITAS TRANSAKSI DUA TABEL
# ============================================================================
print("\n--- PEMBUKTIAN ATOMISITAS (LANGKAH 5) ---")

conn = sqlite3.connect(TEST_DB)
# 1. Cek status awal unit PS4-02: harus 'tersedia'
status_sebelum = conn.execute("SELECT status FROM consoles WHERE id = 2;").fetchone()[0]
assert status_sebelum == "tersedia"
count_trx_sebelum = conn.execute("SELECT COUNT(*) FROM transactions;").fetchone()[0]
conn.close()
print(f"[BUKTI 1] Status unit PS4-02 sebelum sewa: '{status_sebelum}' (Jumlah sewa: {count_trx_sebelum})")

# 2. Catat transaksi sewa berhasil untuk unit PS4-02
success, errors, trx_id = create_transaction("Rian Pratama", 2, 1, user_id=1, db_name=TEST_DB)
assert success is True

conn = sqlite3.connect(TEST_DB)
status_sesudah = conn.execute("SELECT status FROM consoles WHERE id = 2;").fetchone()[0]
count_trx_sesudah = conn.execute("SELECT COUNT(*) FROM transactions;").fetchone()[0]
conn.close()
assert status_sesudah == "terpakai"
assert count_trx_sesudah == count_trx_sebelum + 1
print(f"[BUKTI 2] Status unit PS4-02 sesudah sewa: '{status_sesudah}' (Jumlah sewa bertambah menjadi {count_trx_sesudah})")

# 3. Transaksi gagal dengan ID induk tidak ada (console_id = 999): Buktikan tidak ada jejak parsial
success_fail, errors_fail, _ = create_transaction("Gagal Test", 999, 1, user_id=1, db_name=TEST_DB)
assert success_fail is False

conn = sqlite3.connect(TEST_DB)
count_trx_akhir = conn.execute("SELECT COUNT(*) FROM transactions;").fetchone()[0]
conn.close()
assert count_trx_akhir == count_trx_sesudah
print(f"[BUKTI 3] Transaksi gagal: Jumlah baris transaksi tetap {count_trx_akhir} (Tidak ada jejak parsial)")


# ============================================================================
# LANGKAH 6: UJI PROTEKSI FOREIGN KEY SAAT HAPUS INDUK
# ============================================================================
print("\n--- UJI PROTEKSI FOREIGN KEY (LANGKAH 6) ---")

# Hapus konsol ID 1 yang sudah memiliki transaksi sewa (Andi Saputra)
res_del_used = client.post("/consoles/1/hapus", follow_redirects=True)
assert res_del_used.status_code == 200
assert "tidak dapat dihapus karena memiliki" in res_del_used.text
print("[LULUS] Hapus unit konsol yang sudah dipakai sewa ditolak secara ramah.")

# Cek konsol ID 1 masih tetap ada di database
conn = sqlite3.connect(TEST_DB)
c1 = conn.execute("SELECT id FROM consoles WHERE id = 1;").fetchone()
assert c1 is not None
conn.close()
print("[LULUS] Verifikasi data induk tetap utuh di database.")


# ============================================================================
# LANGKAH 9 & 10: PENCARIAN (q) & PENYARINGAN (status_bayar, jenis_konsol)
# ============================================================================
print("\n--- UJI PENCARIAN & PENYARINGAN (LANGKAH 9 & 10) ---")

# Uji 1: Sebagian nama, huruf besar-kecil berbeda
res_q1 = client.get("/sewa?q=andi")
assert res_q1.status_code == 200
assert "Andi Saputra" in res_q1.text
assert "Rian Pratama" not in res_q1.text
print("[LULUS] Pencarian 1: Case-insensitive 'andi' menampilkan baris yang cocok.")

# Uji 2: Kata yang tidak ada
res_q2 = client.get("/sewa?q=ZzzzzNotFound")
assert res_q2.status_code == 200
assert "Tidak ada transaksi sewa yang cocok" in res_q2.text
print("[LULUS] Pencarian 2: Kata yang tidak ada menampilkan pesan tidak cocok.")

# Uji 3: Karakter % atau _ di-escape secara harfiah
res_q3 = client.get("/sewa?q=%")
assert res_q3.status_code == 200
# Karena tidak ada pelanggan bernama '%' harfiah, tidak boleh menampilkan semua baris layaknya wildcard unescaped
assert "Tidak ada transaksi sewa yang cocok" in res_q3.text
print("[LULUS] Pencarian 3: Tanda % di-escape secara harfiah (bukan wildcard liar).")

# Uji 4: Injeksi SQL ' OR 1=1 --
res_q4 = client.get("/sewa?q=' OR 1=1 --")
assert res_q4.status_code == 200
assert "Tidak ada transaksi sewa yang cocok" in res_q4.text
print("[LULUS] Pencarian 4: Upaya injeksi SQL dinetralkan oleh kueri berparameter.")

# Uji 5: Penggabungan Pencarian dan Penyaringan (?q=Andi&status_bayar=open_bill)
res_combo = client.get("/sewa?q=Andi&status_bayar=open_bill")
assert res_combo.status_code == 200
assert "Andi Saputra" in res_combo.text
print("[LULUS] Penyaringan: Pencarian dan filter status bayar berhasil digabungkan.")

# ============================================================================
# TUGAS LANJUTAN (LANGKAH 16): PENGHENTIAN SEWA & PERHITUNGAN DENDA
# ============================================================================
print("\n--- UJI PENGHENTIAN SEWA & PERHITUNGAN DENDA (LANGKAH 16) ---")

# 1. Penyelesaian sesi sewa normal via POST /sewa/<id>/selesai
res_selesai = client.post("/sewa/1/selesai", follow_redirects=True)
assert res_selesai.status_code == 200
assert "berhasil diselesaikan" in res_selesai.text

# Verifikasi konsol kembali tersedia di basis data
conn_check = sqlite3.connect(TEST_DB)
c_status = conn_check.execute("SELECT status FROM consoles WHERE id = 1;").fetchone()[0]
assert c_status == "tersedia"

# Verifikasi transaksi berstatus lunas dan waktu_selesai terisi
trx_row = conn_check.execute("SELECT status_bayar, waktu_selesai FROM transactions WHERE id = 1;").fetchone()
assert trx_row[0] == "lunas"
assert trx_row[1] is not None
conn_check.close()
print("[LULUS] Penghentian sewa normal: Unit konsol kembali 'tersedia', status transaksi 'lunas'.")

# 2. Penyelesaian sewa dengan denda keterlambatan (Langkah 16)
from services import finish_transaction
# Buka sewa baru untuk pengujian denda
ok, _, trx_denda_id = create_transaction("Candra Wijaya", 1, 1, db_name=TEST_DB)
assert ok is True

# Selesaikan dengan keterlambatan 15 menit
ok_fin, msg_fin, code_fin = finish_transaction(trx_denda_id, force_menit_terlambat=15, db_name=TEST_DB)
assert ok_fin is True
assert code_fin == 200

# Verifikasi tabel fines terisi dengan benar
conn_fines = sqlite3.connect(TEST_DB)
fine_row = conn_fines.execute("SELECT menit_terlambat, biaya_denda FROM fines WHERE transaction_id = ?;", (trx_denda_id,)).fetchone()
assert fine_row is not None
assert fine_row[0] == 15
assert fine_row[1] == 15000  # 15 menit * Rp 1.000 = Rp 15.000
conn_fines.close()

# Verifikasi denda ter-render di tabel antarmuka
res_denda_view = client.get("/sewa")
assert "Denda Rp 15.000" in res_denda_view.text
assert "+15 mnt" in res_denda_view.text
print("[LULUS] Penghentian sewa dengan denda: Tabel fines tercatat akurat dan ter-render di antarmuka.")

# 3. Penyelesaian ganda ditolak
ok_double, msg_double, code_double = finish_transaction(trx_denda_id, db_name=TEST_DB)
assert ok_double is False
assert code_double == 400
print("[LULUS] Penyelesaian transaksi yang sudah selesai ditolak secara ramah.")

print("\n--- SELURUH PENGUJIAN JOBSHEET 10 LULUS 100% ---")

if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
