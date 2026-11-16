import sqlite3
import os

db_path = "test_rental.db"
schema_path = "docs/desain/schema.sql"

# Hapus database uji lama jika ada
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Baca dan eksekusi schema.sql
with open(schema_path, "r", encoding="utf-8") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
conn.commit()

print("--- MENJALANKAN UJI PELANGGARAN SKEMA ---")

# Daftar uji pelanggaran (Harus ditolak / memunculkan IntegrityError)
uji_pelanggaran = [
    ("Uji 1: Insert harga paket negatif", 
     "INSERT INTO packages (nama_paket, durasi_menit, harga) VALUES ('Paket Gagal', 60, -5000);"),
    
    ("Uji 2: Insert Foreign Key yang tidak ada (konsol invalid)", 
     "INSERT INTO transactions (user_id, console_id, package_id, waktu_mulai) VALUES (1, 999, 1, '2026-11-14 10:00:00');"),
    
    ("Uji 3: Insert nilai UNIQUE ganda (username sama)", 
     "INSERT INTO users (username, password_hash, role) VALUES ('admin', 'hash1', 'kasir');")
]

# Masukkan data valid awal agar uji FK/unik berjalan semestinya
cursor.execute("INSERT INTO users (username, password_hash, role) VALUES ('admin', 'hash1', 'kasir');")
cursor.execute("INSERT INTO consoles (kode_konsol, jenis_konsol, status) VALUES ('PS4-01', 'PS4', 'tersedia');")
cursor.execute("INSERT INTO packages (nama_paket, durasi_menit, harga) VALUES ('Paket 1 Jam', 60, 10000);")
conn.commit()

for deskripsi, sql_query in uji_pelanggaran:
    try:
        cursor.execute(sql_query)
        conn.commit()
        print(f"[GAGAL] {deskripsi} -> Seharusnya ditolak, tetapi BERHASIL dieksekusi!")
    except sqlite3.IntegrityError as e:
        print(f"[OK DITOLAK] {deskripsi} -> Error tertangkap: {e}")

conn.close()
if os.path.exists(db_path):
    os.remove(db_path)