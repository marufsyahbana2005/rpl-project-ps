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

### 2.2 Sprint 2 (Minggu 11 – 12): Siklus Transaksi, Dasbor Monitoring, dan Timer Real-Time
- **Fokus Utama:** Penyempurnaan siklus hidup sewa, monitoring ketersediaan konsol secara real-time, dan audit keamanan.
- **Butir Backlog:**
  - [ ] Dasbor monitoring ketersediaan konsol *real-time* via *HTTP polling* 10 detik (**KF-04**).
  - [ ] Visualisasi timer mundur (*countdown timer*) sesi sewa berjalan di antarmuka kasir.
  - [ ] Fitur pembatalan sewa darurat (kasus mati lampu / kendala teknis $< 5$ menit pertama).
  - [ ] Ekspor rekapitulasi sesi sewa harian ke format CSV / cetak nota struk kasir.
- 🚩 **TARGET CHECKPOINT MINGGU 12:**
  - Audit Keamanan Menyeluruh: Pengujian injeksi SQL lanjutan, pengujian penetrasi CSRF/XSS, dan pembatasan otentikasi peran kasir vs owner.
  - *Peer Code Review* lintas kelompok terhadap seluruh perubahan kode Sprint 1 dan Sprint 2.
  - Presentasi demo integrasi Sprint 1 dan Sprint 2 di hadapan dosen pengampu.

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
