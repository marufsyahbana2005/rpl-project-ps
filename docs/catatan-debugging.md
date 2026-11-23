# Catatan Sesi Debugging Terpandu (Langkah 11) — Exito Playbox

Dokumen ini memuat catatan dua insiden kesalahan pemrograman dan alur investigasi sistematis (6 langkah debugging) yang dilakukan pada sesi latihan debugging.

---

## Kasus Debug 1: `sqlite3.OperationalError: no such column: c.nama_konsol`
- **Penyisip Masalah:** Simulasi Pengembang A
- **Investigator:** Maruf Syahbana (Pengembang B)

### 1. Gejala dan Reproduksi
Saat mengakses rute `/sewa` untuk menampilkan daftar transaksi sewa, server mengembalikan respon HTTP 500 *Internal Server Error*.
```
Traceback (most recent call last):
  File "app.py", line 185, in daftar_sewa
    transactions = get_all_transactions()
  File "services.py", line 280, in get_all_transactions
    return conn.execute(sql, params).fetchall()
sqlite3.OperationalError: no such column: c.nama_konsol
```

### 2. Analisis Frame dan Hipotesis
- **Frame Milik Sendiri:** `services.py` baris 280 pada pemanggilan kueri SQL.
- **Hipotesis:** Kueri JOIN mencoba memilih kolom `c.nama_konsol` dari alias tabel `consoles`. Padahal berdasarkan dokumen `docs/desain/schema.sql` dan kamus data, kolom identitas unit fisik PlayStation bernama `kode_konsol`, bukan `nama_konsol`.

### 3. Prompt Konteks ke AI
> *"Konteks: Pada fungsi get_all_transactions() di services.py, muncul pesan error 'sqlite3.OperationalError: no such column: c.nama_konsol'. Skema tabel consoles memiliki kolom: id, kode_konsol, jenis_konsol, status. Mengapa error ini terjadi dan bagaimana solusinya?"*

### 4. Penjelasan Penyebab & Solusi Perbaikan
- **Penyebab:** Kesalahan ketik (*typo*) pada klausa `SELECT` kueri SQL di mana atribut entitas induk salah diasumsikan sebagai `nama_konsol`.
- **Perbaikan:** Mengubah `c.nama_konsol` menjadi `c.kode_konsol` pada `services.py`.
- **Uji Pencegah:** Menjalankan `python tests/uji_cepat.py` untuk memastikan seluruh kueri JOIN dievaluasi otomatis sebelum rilis.

---

## Kasus Debug 2: Gagal Menemukan Unit Konsol Akibat Masukan String ID
- **Penyisip Masalah:** Simulasi Pengembang B
- **Investigator:** Maruf Syahbana (Pengembang A)

### 1. Gejala dan Reproduksi
Saat mengirim form buka sewa dari browser, sistem selalu memunculkan pesan galat *"Unit konsol dengan ID # tidak ditemukan di sistem"* meskipun pilihan unit pada dropdown sudah dipilih.

### 2. Analisis Frame dan Hipotesis
- **Frame Milik Sendiri:** `services.py` fungsi `create_transaction()`.
- **Hipotesis:** Nilai `console_id` yang diterima dari `request.form.get('console_id')` bertipe data string mentah (atau string kosong jika atribut name pada HTML salah). Di sisi SQLite, kueri `SELECT id FROM consoles WHERE id = ?` jika dibandingkan dengan string yang tidak di-cast ke integer dapat memicu ketidakcocokan tipe atau bypass validasi.

### 3. Prompt Konteks ke AI
> *"Konteks: Form POST /sewa/buka mengirim nilai console_id. Mengapa kueri pengecekan konsol gagal menemukan baris padahal ID ada di tabel? Kode: c_id = console_id; console = conn.execute('SELECT id, status FROM consoles WHERE id = ?', (c_id,)).fetchone()".*

### 4. Penjelasan Penyebab & Solusi Perbaikan
- **Penyebab:** Masukan form HTML selalu berupa string. Perlu konversi tipe data yang aman menggunakan blok `try...except ValueError` (`c_id = int(console_id)`), serta pengecekan apakah dropdown bernilai string kosong.
- **Perbaikan:** Menambahkan sanitasi konversi tipe data dan pesan validasi spesifik: *"Pilih unit konsol yang valid dari daftar"*.
- **Uji Pencegah:** Kasus uji TC-5 pada `tests/test_transaksi_berelasi.py` (uji masukan `console_id = 'abc'`).
