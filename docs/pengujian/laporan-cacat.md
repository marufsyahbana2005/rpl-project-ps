# Laporan Cacat dan Permintaan Perubahan (Jobsheet 13 — Lampiran B.3)

Dokumen ini memuat daftar temuan cacat (*software defects*) dan permintaan perubahan (*change requests*) yang teridentifikasi dari hasil uji eksploratif (*exploratory testing*) pada sistem **Exito Playbox** (`rpl-project-ps`).

---

## 1. Daftar Temuan Cacat (Defect Reports)

### Cacat 1: D-01 — Penanganan Tipe Masukan Non-String pada `nama_pelanggan` Memicu HTTP 500 (AttributeError)

- **ID Cacat:** `D-01`
- **Modul / Komponen:** `services.py` $\rightarrow$ `_validate_transaction_payload()` & `create_transaction()`
- **Kebutuhan Terkait:** `KF-08` (Validasi Masukan Form Transaksi)
- **Tingkat Keparahan (*Severity*):** **Tinggi (High)** — Menyebabkan *Unhandled Exception* dan *crash* HTTP 500 Internal Server Error.
- **Prioritas (*Priority*):** **Tinggi (P1)**
- **Status:** **Diperbaiki (Fixed)** — Commit `16db5e1`
- **Uji Regresi:** `tests/test_cacat.py::test_cacat_d01_nama_pelanggan_non_string_handled_safely` (Status: LULUS)
- **Langkah Reproduksi:**
  1. Panggil fungsi layanan `create_transaction(nama_pelanggan=12345, console_id=1, package_id=1)` secara langsung atau kirim payload non-string.
  2. Fungsi `_validate_transaction_payload()` mengeksekusi `(nama_pelanggan or "").strip()`.
  3. Python melemparkan `AttributeError: 'int' object has no attribute 'strip'`.
- **Hasil Aktual Sebelum Perbaikan:** Aplikasi crash dengan `AttributeError: 'int' object has no attribute 'strip'` (HTTP 500).
- **Hasil Aktual Sesudah Perbaikan:** Masukan integer dinormalisasi dengan `str(nama_pelanggan)` dan transaksi tersimpan sukses tanpa crash.
- **Hasil yang Diharapkan:** Masukan dinormalisasi secara aman menjadi string `str(nama_pelanggan or "").strip()` dan divalidasi panjang karakternya tanpa melempar eksepsi.

---

### Cacat 2: D-02 — Duplikasi Nama Paket Sewa Berbeda Huruf Besar-Kecil (*Case-Insensitive Bypass*)

- **ID Cacat:** `D-02`
- **Modul / Komponen:** `services.py` $\rightarrow$ `create_package()` & `update_package()`
- **Kebutuhan Terkait:** `KF-02` (Kalkulasi Paket Sewa) & `KF-08` (Integritas Data Master)
- **Tingkat Keparahan (*Severity*):** **Sedang (Medium)** — Menyebabkan data ganda (*duplicate data anomaly*) pada tabel paket.
- **Prioritas (*Priority*):** **Sedang (P2)**
- **Status:** **Diperbaiki (Fixed)** — Commit `f7f17d9`
- **Uji Regresi:** `tests/test_cacat.py::test_cacat_d02_duplikasi_nama_paket_case_insensitive` (Status: LULUS)
- **Langkah Reproduksi:**
  1. Daftarkan paket sewa baru dengan nama `"Reguler 1 Jam"` (berhasil tersimpan).
  2. Daftarkan paket sewa kedua dengan nama `"reguler 1 jam"` atau `"REGULER 1 JAM"`.
  3. Sistem SQLite mengeksekusi `SELECT id FROM packages WHERE nama_paket = ?;` yang secara baku membandingkan secara *case-sensitive*.
- **Hasil Aktual Sebelum Perbaikan:** Dua paket dengan nama yang secara semantik identik berhasil tersimpan bersamaan di database (`assert True is False`).
- **Hasil Aktual Sesudah Perbaikan:** Kueri membandingkan via `LOWER(nama_paket) = LOWER(?)`, menolak paket kedua dengan pesan ramah.
- **Hasil yang Diharapkan:** Kueri validasi duplikasi membandingkan secara case-insensitive: `WHERE LOWER(nama_paket) = LOWER(?)`, menolak pendaftaran paket kedua dengan pesan: `"Nama paket 'reguler 1 jam' sudah digunakan."`.

---

### Cacat 3: D-03 — Pemilik Dapat Mengubah Status Konsol yang Sedang Disewa Aktif (`terpakai`)

- **ID Cacat:** `D-03`
- **Modul / Komponen:** `services.py` $\rightarrow$ `update_console()` & `app.py`
- **Kebutuhan Terkait:** `KF-01` (Integritas Status Unit Konsol) & `KF-08` (Validasi Konsistensi Data)
- **Tingkat Keparahan (*Severity*):** **Tinggi (High)** — Merusak integritas data operasional bisnis (konsol berstatus maintenance padahal timer sewa pelanggan sedang berjalan).
- **Prioritas (*Priority*):** **Tinggi (P1)**
- **Status:** **Diperbaiki (Fixed)** — Commit `60f2567`
- **Uji Regresi:** `tests/test_cacat.py::test_cacat_d03_ubah_status_konsol_terpakai_ditolak` (Status: LULUS)
- **Langkah Reproduksi:**
  1. Kasir membuka sewa untuk unit `"PS4-01"` sehingga status unit menjadi `'terpakai'`.
  2. Pemilik membuka halaman ubah unit konsol `/consoles/<id>/ubah`.
  3. Pemilik mengubah status unit menjadi `'maintenance'` dan menekan Simpan.
- **Hasil Aktual Sebelum Perbaikan:** Fungsi `update_console()` memperbarui status unit menjadi `'maintenance'` (`assert True is False`).
- **Hasil Aktual Sesudah Perbaikan:** Pengecekan `current["status"] == "terpakai"` menolak perubahan dengan HTTP 400 dan pesan spesifik.
- **Hasil yang Diharapkan:** Sistem menolak pengubahan status manual bila `current["status"] == "terpakai"`, dengan pesan galat: `"Unit konsol sedang dalam sesi sewa aktif dan statusnya tidak dapat diubah secara manual."`.

---

## 2. Daftar Permintaan Perubahan (Change Requests — CR)

Tabel berikut mencatat usulan penyempurnaan fitur yang sesuai dengan spesifikasi PRD tetapi disarankan untuk ditingkatkan pada rilis berikutnya:

| ID CR | Modul Terkait | Deskripsi Usulan Perubahan | Alasan Bisnis & Manfaat | Prioritas |
|:---:|---|---|---|:---:|
| `CR-01` | Antarmuka Kasir | Penambahan dialog konfirmasi visual (JavaScript modal) sebelum kasir menekan tombol "Selesaikan Sewa". | Mencegah penekanan tombol tidak sengaja yang dapat menghentikan sesi sewa pelanggan sebelum waktunya. | Medium |
| `CR-02` | Master Paket | Fitur penyaringan pencarian teks pada tabel paket sewa di halaman pemilik. | Memudahkan pemilik rental mencari paket sewa tertentu saat variasi paket bertambah banyak. | Low |
| `CR-03` | Cetak Struk | Tombol pintas untuk mencetak nota struk fisik/PDF sesaat setelah transaksi sewa selesai. | Memenuhi kebutuhan pelanggan yang meminta bukti fisik pembayaran sewa dan denda. | Medium |
