# Rencana Sprint 1–4 (RTM-2) — Exito Playbox

Dokumen ini memuat rencana pelaksanaan Sprint 1 sampai Sprint 4 untuk penyusunan Rilis Tugas Mandiri 2 (RTM-2), ringkasan evaluasi jurnal vibe coding, penetapan target *checkpoint* Minggu 12, serta pembagian penugasan fitur untuk Pertemuan 10.

---

## 1. Evaluasi Jurnal Vibe Coding dan Proporsi Keputusan
Hingga akhir pengerjaan Pertemuan 10 (implementasi modul berelasi `transactions`, transaksi multi-tabel atomik, pencarian & penyaringan, 2 sesi debugging, refactoring, dan penghentian sewa/denda), tercatat total **20 entri log** pada `jurnal-vibe-coding.md`:

| Kategori Keputusan | Jumlah Entri | Persentase | Keterangan Evaluasi Praktik Vibe Coding |
|:--:|:--:|:--:|---|
| **Terima** | 20 | 100% | Seluruh hasil generasi kode AI diuji dengan skrip uji regresi otomatis (`tests/uji_cepat.py` & `tests/test_transaksi_berelasi.py`), mematuhi arsitektur 3-tier, serta menerapkan query SQL berparameter dan proteksi XSS Jinja2. |
| **Ubah** | 0 | 0% | Perbaikan kecil (penyesuaian tipe string ID konsol dan perbaikan typo kolom JOIN `c.kode_konsol`) dituntaskan secara langsung melalui sesi investigasi debugging terpandu (Entri 17, 18, dan 19). |
| **Tolak** | 0 | 0% | Tidak ada kode AI yang ditolak mentah-mentah karena pengembang konsisten memberikan prompt terarah yang menyertakan potongan `schema.sql` dan batasan `aturan-proyek.md`. |

---

## 2. Rencana Pelaksanaan Sprint 1–4 (RTM-2)

Rencana sprint ini diturunkan langsung dari dokumen `docs/product-backlog.md`, PRD, dan SRS sistem Exito Playbox:

### 2.1 Sprint 1 (Minggu 9 – 10): Fondasi Kerangka, Master Data, & Modul Berelasi
- **Fokus Utama:** Pembangunan kerangka kerja aplikasi Flask, inisialisasi basis data SQLite, manajemen entitas master, serta modul transaksi sewa berelasi.
- **Butir Backlog yang Diselesaikan (Pertemuan 9 & 10):**
  - [x] Inisialisasi basis data SQLite otomatis dari `docs/desain/schema.sql` (`models.py`).
  - [x] Kerangka kerja Flask 3-tier, kunci rahasia aman, dan templat dasar responsif (`base.html`).
  - [x] Modul CRUD lengkap entitas pertama: Unit Konsol (`consoles`) — F1 s/d F5.
  - [x] Modul CRUD lengkap entitas kedua: Paket Sewa (`packages`) — Siklus CRUD terpisah.
  - [x] Rangkaian pengujian unit otomatis master data (`test_tambah_konsol.py`, `test_crud_konsol.py`, `test_crud_packages.py`).
  - [x] Modul relasi transaksi sewa (`transactions`) dengan JOIN multi-tabel (`consoles`, `packages`, `users`) — G1.
  - [x] Form buka sewa kasir dengan pilihan entitas induk dan validasi nilai batas — G2.
  - [x] Transaksi atomik multi-tabel: pencatatan sewa & perubahan status konsol menjadi `'terpakai'` (**KF-01**) — G3.
  - [x] Pencarian LIKE berparameter (escape `%`, `_`) dan penyaringan dinamis multi-kriteria (`status_bayar`, `jenis_konsol`) — G4.
  - [x] Skrip uji regresi otomatis mandiri `tests/uji_cepat.py` (Langkah 12).
  - [x] Penghentian sesi sewa kasir (`POST /sewa/<id>/selesai`), pengembalian status unit konsol menjadi `'tersedia'`, dan pencatatan denda otomatis ke tabel `fines` (**KF-03**).

---

### 2.2 Sprint 2 (Minggu 11 – 12): Siklus Transaksi, Autentikasi RBAC, dan Bahan Checkpoint Minggu 12
- **Fokus Utama:** Pengamanan hak akses berbasis peran, siklus hidup transaksi, serta persiapan demonstrasi checkpoint Minggu 12.
- **Butir Backlog yang Diselesaikan (Pertemuan 11):**
  - [x] Autentikasi login aman dengan kata sandi ter-hash scrypt/pbkdf2 ber-salt unik (**H1**).
  - [x] Rute login netral (anti-user enumeration), pembersihan sesi `session.clear()`, dan proteksi logout POST (**H2**).
  - [x] Sanitasi parameter `next` anti-Open Redirect (**H2**).
  - [x] Decorator otorisasi peran `@login_diperlukan` dan `@peran_diperlukan` di tingkat server (**H3**).
  - [x] Halaman galat informatif 403 Forbidden (`403.html`).
  - [x] Templat induk `base.html` dinamis menyesuaikan peran dan styling CSS terpusat `static/style.css` (**H4**).
  - [x] Validasi masukan dua lapis (HTML5 sisi klien + sanitasi ketat sisi server) (**H5**).
  - [x] Skrip uji otomatis mandiri diperluas dengan 6 pengujian autentikasi & peran (`tests/uji_cepat.py`).

- 🚩 **SUSUNAN BAHAN DEMO CHECKPOINT MINGGU 12 (PROTOTIPE 5 MENIT):**
  1. **Menit 00:00 – 01:00 (Alur Tamu & Login Kasir):**
     - Membuka URL aplikasi sebagai tamu -> otomatis dialihkan ke `/login?next=...`.
     - Masuk menggunakan akun kasir (`kasir_andi` / `andi12345`).
     - Memperlihatkan menu navigasi kasir yang disederhanakan (hanya Sewa Konsol, Buka Sewa, dan Unit Konsol).
  2. **Menit 01:00 – 02:00 (Operasional Transaksi Sewa & Atomisitas):**
     - Mengisi form buka sewa baru untuk pelanggan di unit PS5.
     - Memperlihatkan dampak atomik: unit langsung berstatus `'terpakai'` dan tidak dapat disewa ulang.
  3. **Menit 02:00 – 03:00 (Pembuktian Pertahanan Otorisasi Server):**
     - Membuka URL terlarang secara manual (`/packages` atau `/consoles/tambah`).
     - Menunjukkan halaman 403 Forbidden yang ramah dan aman.
     - Mencoba mengirim POST hapus konsol via alat pengembang/curl -> terblokir 403 dan data basis data tetap utuh.
  4. **Menit 03:00 – 04:00 (Penghentian Sewa Kasir & Login Pemilik):**
     - Kasir menghentikan sesi sewa -> kalkulasi denda keterlambatan otomatis masuk ke tabel `fines`, status konsol pulih `'tersedia'`.
     - Kasir logout -> login sebagai Pemilik (`owner_hendra` / `hendra12345`).
     - Memperlihatkan hak akses penuh: menu Paket Sewa dan tombol Kelola Unit Konsol aktif.
  5. **Menit 04:00 – 05:00 (Audit Kriptografi & Uji Regresi Mandiri):**
     - Membuka SQLite untuk membuktikan kata sandi tersimpan sebagai hash acak ber-salt (`scrypt:...`), bukan teks asli.
     - Menjalankan `python tests/uji_cepat.py` dari terminal -> membuktikan `"SEMUA UJI LULUS"` secara langsung di depan evaluator.

- 📋 **DAFTAR FITUR TERTUNDA & RENCANA PENYELESAIAN (PERTEMUAN 12):**
  1. *Rate Limiting Login (Maks. 5x percobaan per 15 menit):* Selesai pada Pertemuan 12 dengan modul counter berbasis memori/IP.
  2. *Token CSRF Tersembunyi pada Form POST:* Integrasi perlindungan CSRF pada seluruh form mutasi data.
  3. *Session Idle Timeout (30 Menit):* Penambahan konfigurasi `PERMANENT_SESSION_LIFETIME` pada `app.py`.
  4. *Dasbor Polling Konsol Real-Time (KF-04):* Polling interval 10 detik menggunakan JavaScript Fetch API tanpa reload halaman.

---

### 2.3 Sprint 3 (Minggu 13 – 14): Rekapitulasi Laporan Finansial & Audit Transaksi
- **Fokus Utama:** Transparansi keuangan bagi pemilik rental dan ketahanan audit data.
- **Butir Backlog:**
  - [ ] Modul rekapitulasi laporan pendapatan harian dan bulanan otomatis (**KF-06**).
  - [ ] Pembatasan rute laporan keuangan (*Role-Based Access Control* khusus peran `owner`, **KNF-03**).
  - [ ] Modul penelusuran riwayat nota transaksi sewa lengkap dengan pencarian nama pelanggan dan tanggal (**KF-07**, **KF-10**).
  - [ ] Validasi ketat masukan form kasir untuk mencegah data kosong (**KF-08**).

---

### 2.4 Sprint 4 (Minggu 15 – 16): Polish Antarmuka, UAT Klien, & Rilis Final
- **Fokus Utama:** Pengujian penerimaan akhir bersama klien dan finalisasi dokumentasi.
- **Butir Backlog:**
  - [ ] Pencatatan inventaris aksesori pendukung stik dan kabel (**KF-09**).
  - [ ] Optimalisasi performa pemuatan antarmuka agar selalu $\le 2$ detik (**KNF-01**).
  - [ ] Eksekusi skenario *User Acceptance Testing* (UAT) bersama pemilik Exito Playbox (Bpk. Hendra).
  - [ ] Penyusunan Laporan Akhir Proyek dan rilis versi v1.0.

---

## 3. Evaluasi Capaian Pertemuan 10 & Rencana Pertemuan 11

Seluruh penugasan Pertemuan 10 (Sprint 1 Fase 2) telah selesai 100%:

| No | Modul / Fitur | Status Capaian | Bukti Pengujian | Penanggung Jawab |
|:--:|---|:--:|---|:--:|
| **1** | **Model & Service Transaksi (`transactions`)** | **Selesai (100%)** | `tests/test_transaksi_berelasi.py` (Atomisitas & JOIN) | Maruf Syahbana |
| **2** | **Antarmuka Form Buka Sewa & Daftar Sewa** | **Selesai (100%)** | `templates/daftar_sewa.html` & `templates/buka_sewa.html` | Maruf Syahbana |
| **3** | **Skrip Uji Cepat Regresi (`uji_cepat.py`)** | **Selesai (100%)** | Menghasilkan output `"SEMUA UJI LULUS"` | Maruf Syahbana |
| **4** | **Fitur Penghentian Sewa & Denda (`fines`)** | **Selesai (100%)** | Verifikasi tabel `fines` dan status unit kembali `'tersedia'` | Maruf Syahbana |
