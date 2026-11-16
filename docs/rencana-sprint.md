# Rencana Sprint 1–4 (RTM-2) — Exito Playbox

Dokumen ini memuat rencana pelaksanaan Sprint 1 sampai Sprint 4 untuk penyusunan Rilis Tugas Mandiri 2 (RTM-2), ringkasan evaluasi jurnal vibe coding, penetapan target *checkpoint* Minggu 12, serta pembagian penugasan fitur untuk Pertemuan 10.

---

## 1. Evaluasi Jurnal Vibe Coding dan Proporsi Keputusan
Hingga akhir pengerjaan Sesi 1 dan Sesi 2 (implementasi modul CRUD entitas pertama `consoles` dan entitas kedua `packages`), tercatat total **11 entri log** pada `jurnal-vibe-coding.md`:

| Kategori Keputusan | Jumlah Entri | Persentase | Keterangan Evaluasi |
|:--:|:--:|:--:|---|
| **Terima** | 11 | 100% | Seluruh keluaran AI diawali prompt dengan batasan spesifik (*prompt engineering* terarah), diverifikasi melalui baris-demi-baris kode, dan diuji menggunakan skrip otomatis unit/skema sebelum disetujui. |
| **Ubah** | 0 | 0% | Penyesuaian kecil (seperti path impor test dan Jinja2 uppercase escape) langsung diselesaikan dalam siklus debugging terkendali. |
| **Tolak** | 0 | 0% | Tidak ada usulan pustaka eksternal ilegal atau perusakan skema basis data karena batasan arsitektur telah dikunci sejak awal pada `aturan-proyek.md`. |

---

## 2. Rencana Pelaksanaan Sprint 1–4 (RTM-2)

Rencana sprint ini diturunkan langsung dari dokumen `docs/product-backlog.md`, PRD, dan SRS sistem Exito Playbox:

### 2.1 Sprint 1 (Minggu 9 – 10): Fondasi Kerangka & Master Data
- **Fokus Utama:** Pembangunan kerangka kerja aplikasi Flask, inisialisasi basis data SQLite, dan manajemen entitas master independen.
- **Butir Backlog yang Diselesaikan (Pertemuan 9):**
  - [x] Inisialisasi basis data SQLite otomatis dari `docs/desain/schema.sql` (`models.py`).
  - [x] Kerangka kerja Flask 3-tier, kunci rahasia aman, dan templat dasar responsif (`base.html`).
  - [x] Modul CRUD lengkap entitas pertama: Unit Konsol (`consoles`) — F1 s/d F5.
  - [x] Modul CRUD lengkap entitas kedua: Paket Sewa (`packages`) — Langkah 14.
  - [x] Rangkaian pengujian unit otomatis (`tests/test_tambah_konsol.py`, `tests/test_crud_konsol.py`, `tests/test_crud_packages.py`).
- **Target Lanjutan Sprint 1 (Pertemuan 10):**
  - [ ] Pembuatan modul relasi transaksi sewa (`transactions`) yang menghubungkan unit konsol, kasir, dan paket durasi.
  - [ ] Implementasi form kasir untuk membuka sesi sewa dan mengubah status konsol menjadi `'terpakai'` secara atomik (**KF-01**).
  - [ ] Penerapan logika kalkulasi estimasi durasi dan tarif biaya sewa otomatis (**KF-02**).

---

### 2.2 Sprint 2 (Minggu 11 – 12): Siklus Transaksi, Timer, dan Denda Overtime
- **Fokus Utama:** Penyempurnaan siklus hidup sewa, monitoring real-time, dan penanganan kelebihan waktu.
- **Butir Backlog:**
  - [ ] Dasbor monitoring ketersediaan konsol *real-time* via *HTTP polling* 10 detik (**KF-04**).
  - [ ] Modul penghentian timer sewa dan kalkulasi otomatis denda keterlambatan dengan aturan toleransi *grace period* 5 menit (**KF-03**).
  - [ ] Fitur penyaringan (*filtering*) daftar unit konsol berdasarkan jenis PlayStation (**KF-05**).
  - [ ] Fitur pembatalan sewa darurat (kasus mati lampu / kendala teknis $< 5$ menit pertama).
- 🚩 **TARGET CHECKPOINT MINGGU 12:**
  - Audit Keamanan Menyeluruh: Pengujian injeksi SQL lanjutan, pengujian penetrasi CSRF/XSS, dan pembatasan otentikasi peran kasir vs owner.
  - *Peer Code Review* lintas kelompok terhadap seluruh perubahan kode Sprint 1 dan Sprint 2.

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

## 3. Pembagian Tugas untuk Pertemuan 10 (Minggu Depan)

Pada Pertemuan 10, pekerjaan difokuskan pada penyelesaian separuh kedua Sprint 1 (Relasi Transaksi Sewa & Logika Billing):

| No | Modul / Fitur | Deskripsi Pekerjaan | Kebutuhan Terkait | Penanggung Jawab |
|:--:|---|---|:--:|---|
| **1** | **Model & Service Transaksi (`transactions`)** | Membuat fungsi `create_transaction()` pada `services.py` yang memvalidasi `console_id` berstatus `'tersedia'`, mengikat `package_id`, mencatat waktu mulai, dan mengubah status konsol menjadi `'terpakai'` dalam satu transaksi basis data (*atomic transaction*). | **KF-01, KF-02** | Maruf Syahbana |
| **2** | **Antarmuka Form Buka Sewa** | Membangun rute `/sewa/buka` dan templat `buka_sewa.html` sesuai wireframe `wf-03`, memuat input nama pelanggan dan dropdown dinamis paket sewa yang tersaring menurut tipe konsol terpilih. | **KF-01, KF-08** | Maruf Syahbana |
| **3** | **Skrip Uji Otomatis Sesi Sewa** | Menyusun berkas `tests/test_transaksi_sewa.py` untuk menguji penolakan sewa pada konsol yang sedang terpakai, validasi nama kosong, dan verifikasi perhitungan waktu selesai. | **KF-01, KF-02** | Maruf Syahbana |
