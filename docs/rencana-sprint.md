# Rencana Sprint 1–4 (RTM-2) — Exito Playbox

Dokumen ini memuat rencana pelaksanaan Sprint 1 sampai Sprint 4 untuk penyusunan Rilis Tugas Mandiri 2 (RTM-2), ringkasan evaluasi jurnal vibe coding, penetapan target *checkpoint* Minggu 12, evaluasi capaian Pertemuan 11 & 12, serta spesifikasi detail persiapan Sprint 3 (Minggu 13–14).

---

## 1. Evaluasi Jurnal Vibe Coding dan Proporsi Keputusan
Hingga akhir pengerjaan Pertemuan 12 (Pengerasan Keamanan OWASP Top 10, Proteksi CSRF Token, Rate Limiting Login, Audit Logging, Secure Headers, Cookie Flags, serta Gladi Demo Checkpoint 5 Menit), tercatat total **37 entri log** pada `jurnal-vibe-coding.md`:

| Kategori Keputusan | Jumlah Entri | Persentase | Keterangan Evaluasi Praktik Vibe Coding |
|:--:|:--:|:--:|---|
| **Terima** | 35 | 94.6% | Hasil generasi kode AI memenuhi standar arsitektur 3-tier, menerapkan query berparameter, lulus skrip uji regresi otomatis (`tests/uji_cepat.py`), dan mematuhi batasan kamus data serta DDL basis data. |
| **Ubah** | 2 | 5.4% | Entri 29 (perbaikan hash naif AI menjadi scrypt/pbkdf2 dan pemindahan penjagaan RBAC dari UI ke backend) serta Entri 36 (penolakan perbaikan CSRF pihak ketiga dari AI dan penyesuaian mekanisme token asli berbasis session). |
| **Tolak** | 0 | 0.0% | Tidak ada kode AI yang ditolak mentah-mentah karena pengembang konsisten memberikan prompt terarah berkonteks potongan kode, batasan keamanan, dan skema basis data. |

---

## 2. Rencana Pelaksanaan Sprint 1–4 (RTM-2)

Rencana sprint ini diturunkan langsung dari dokumen `docs/product-backlog.md`, PRD, dan SRS sistem Exito Playbox:

### 2.1 Sprint 1 (Minggu 9 – 10): Fondasi Kerangka, Master Data, & Modul Berelasi
- **Fokus Utama:** Pembangunan kerangka kerja aplikasi Flask, inisialisasi basis data SQLite, manajemen entitas master, serta modul transaksi sewa berelasi.
- **Status:** **SELESAI 100% (Pertemuan 9 & 10)**
- **Butir Backlog yang Diselesaikan:**
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

### 2.2 Sprint 2 (Minggu 11 – 12): Autentikasi RBAC, Pengerasan Keamanan, & Checkpoint Minggu 12
- **Fokus Utama:** Pengamanan hak akses berbasis peran, pengerasan sistem terhadap OWASP Top 10, perlindungan CSRF, rate limiting, dan demonstrasi checkpoint Minggu 12.
- **Status:** **SELESAI 100% (Pertemuan 11 & 12)**
- **Butir Backlog yang Diselesaikan:**
  - [x] Autentikasi login aman dengan kata sandi ter-hash scrypt/pbkdf2 ber-salt unik (**H1**).
  - [x] Rute login netral (anti-user enumeration), pembersihan sesi `session.clear()`, dan proteksi logout POST (**H2**).
  - [x] Sanitasi parameter `next` anti-Open Redirect (**H2**).
  - [x] Decorator otorisasi peran `@login_diperlukan` dan `@peran_diperlukan` di tingkat server (**H3**).
  - [x] Halaman galat informatif 403 Forbidden (`403.html`).
  - [x] Templat induk `base.html` dinamis menyesuaikan peran dan styling CSS terpusat `static/style.css` (**H4**).
  - [x] Validasi masukan dua lapis (HTML5 sisi klien + sanitasi ketat sisi server) (**H5**).
  - [x] Laporan audit keamanan OWASP Top 10 & pembuktian eksploitasi (`docs/laporan-temuan.md`).
  - [x] Perlindungan CSRF token otomatis pada seluruh form `POST` dan middleware penolakan HTTP 400 (`templates/400_csrf.html`).
  - [x] Proteksi Rate Limiting percobaan login (maksimal 5 kali gagal / 5 menit $\rightarrow$ HTTP 429).
  - [x] Audit Logging keamanan transaksi dan autentikasi tanpa mencatat password plaintext.
  - [x] Konfigurasi produksi: larangan fallback `SECRET_KEY` di produksi, cookie flags (`HttpOnly`, `SameSite=Lax`, `Secure`), dan Security Headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
  - [x] Skrip gladi demo checkpoint 5 menit (`docs/skrip-demo.md`).
  - [x] Skrip uji regresi mandiri `tests/uji_cepat.py` mencakup seluruh aspek keamanan baru (Output: `"SEMUA UJI LULUS"`).

---

### 2.3 Sprint 3 (Minggu 13 – 14): Rekapitulasi Laporan Finansial, Audit Transaksi, & Pengujian Komprehensif
- **Fokus Utama:** Transparansi keuangan bagi pemilik rental, ketahanan audit data, dan eksekusi $\ge 20$ skenario pengujian komprehensif serta User Acceptance Testing (UAT).
- **Target Periode:** Minggu 13 – 14 (Pertemuan 13 & 14)
- **Butir Backlog yang Direncanakan:**
  - [ ] **Modul Rekapitulasi Laporan Pendapatan (KF-06):**
    - Rangkuman total omset pendapatan harian, mingguan, dan bulanan.
    - Pembagian pendapatan sewa pokok vs penerimaan denda keterlambatan (`fines`).
    - Kueri agregasi SQL efisien: `SUM(p.harga)`, `SUM(f.jumlah_denda)`, `COUNT(t.id)`.
  - [ ] **Pembatasan Hak Akses Khusus Pemilik (KNF-03):**
    - Rute `/laporan` dan API agregasi dikunci dengan `@peran_diperlukan('owner')`.
    - Kasir yang mengakses laporan keuangan otomatis terblokir HTTP 403.
  - [ ] **Penelusuran Riwayat Nota Transaksi Lengkap (KF-07, KF-10):**
    - Halaman arsip transaksi riwayat sewa lampau (`status_bayar = 'lunas'`).
    - Pencarian fleksibel berdasarkan rentang tanggal (`tanggal_mulai` s/d `tanggal_selesai`).
    - Fitur cetak nota struk digital / ringkasan transaksi ramah printer (*print stylesheet*).
  - [ ] **Ekspor Data Finansial (Owner Feature):**
    - Kemampuan mengunduh laporan pendapatan dalam format CSV untuk pembukuan eksternal.
  - [ ] **Eksekusi $\ge 20$ Skenario Pengujian Komprehensif:**
    - Melakukan pengujian integrasi ujung-ke-ujung (*end-to-end*), pengujian batas (*boundary value*), dan *negative testing* pada 20 skenario terinci:
      1. TC-01: Login kasir valid $\rightarrow$ Masuk ke dasbor.
      2. TC-02: Login owner valid $\rightarrow$ Masuk ke dasbor lengkap.
      3. TC-03: Login kata sandi salah $\rightarrow$ Pesan galat netral.
      4. TC-04: Login 5x salah $\rightarrow$ Percobaan ke-6 HTTP 429 Too Many Requests.
      5. TC-05: Akses rute `/sewa` tanpa login $\rightarrow$ Redirect ke login.
      6. TC-06: Akses rute `/packages` oleh kasir $\rightarrow$ HTTP 403 Forbidden.
      7. TC-07: POST tanpa token CSRF $\rightarrow$ HTTP 400 Bad Request.
      8. TC-08: POST dengan token CSRF valid $\rightarrow$ Diterima dan diproses.
      9. TC-09: Tambah unit konsol dengan kode valid $\rightarrow$ Tersimpan berstatus 'tersedia'.
      10. TC-10: Tambah unit konsol kode duplikat $\rightarrow$ Ditolak validasi server.
      11. TC-11: Ubah status unit menjadi 'maintenance' oleh owner $\rightarrow$ Status terbarui.
      12. TC-12: Hapus unit konsol bebas transaksi $\rightarrow$ Terhapus sukses.
      13. TC-13: Hapus unit konsol yang sedang/pernah disewa $\rightarrow$ Ditolak ramah (FK Restrict).
      14. TC-14: Buka sewa konsol yang sedang 'terpakai' $\rightarrow$ Tidak muncul di dropdown & ditolak.
      15. TC-15: Transaksi buka sewa baru $\rightarrow$ Atomik mencatat sewa dan mengubah status unit 'terpakai'.
      16. TC-16: Selesai sewa tepat waktu $\rightarrow$ Status unit kembali 'tersedia', denda Rp 0.
      17. TC-17: Selesai sewa terlambat 25 menit $\rightarrow$ Denda tercatat akurat (20 mnt x Rp 1.000).
      18. TC-18: Pencarian transaksi dengan karakter khusus `%` dan `_` $\rightarrow$ Pencarian literal tanpa wildcard bocor.
      19. TC-19: Penyaringan ganda transaksi (status bayar + jenis konsol) $\rightarrow$ Hasil akurat.
      20. TC-20: Akses laporan keuangan oleh owner $\rightarrow$ Menampilkan omset agregat valid.
  - [ ] **Pelaksanaan User Acceptance Testing (UAT):**
    - Sesi simulasi langsung bersama pemilik rental (Bpk. Hendra) menggunakan skenario di atas.
    - Pengisian lembar berita acara penerimaan pengguna (*User Acceptance Form*).

---

### 2.4 Sprint 4 (Minggu 15 – 16): Polish Antarmuka, UAT Klien, & Rilis Final v1.0
- **Fokus Utama:** Penyempurnaan performa, polishing antarmuka pengguna, UAT tahap akhir, dan persiapan rilis v1.0.
- **Butir Backlog:**
  - [ ] Polling inventaris konsol real-time via Fetch API (interval 15 dtk) tanpa reload penuh (**KF-04**).
  - [ ] Pencatatan inventaris aksesori pendukung stik dan kabel (**KF-09**).
  - [ ] Optimalisasi waktu muat halaman agar selalu $\le 2$ detik (**KNF-01**).
  - [ ] Penyusunan Laporan Akhir Proyek dan dokumentasi serah terima sistem.
  - [ ] Rilis Tag Git `v1.0.0-release`.

---

## 3. Evaluasi Capaian Pertemuan 11 & 12

Tabel berikut merangkum pencapaian seluruh modul pada Pertemuan 11 dan 12:

| No | Modul / Fitur | Status Capaian | Bukti Pengujian | Penanggung Jawab |
|:--:|---|:--:|---|:--:|
| **1** | **Autentikasi & Hashing Scrypt (`users`)** | **Selesai (100%)** | `tests/test_autentikasi_peran.py` (KDF terverifikasi) | Maruf Syahbana |
| **2** | **Role-Based Access Control (RBAC)** | **Selesai (100%)** | HTTP 403 Forbidden pada akses rute terlarang | Maruf Syahbana |
| **3** | **Anti-User Enumeration & Open Redirect** | **Selesai (100%)** | Pesan login identik & sanitasi URL `next` | Maruf Syahbana |
| **4** | **Laporan Audit OWASP Top 10** | **Selesai (100%)** | `docs/laporan-temuan.md` (Analisis 10 kasus + 7 audit proyek) | Maruf Syahbana |
| **5** | **Proteksi CSRF Token Formulir POST** | **Selesai (100%)** | HTTP 400 pada manipulasi token di seluruh rute POST | Maruf Syahbana |
| **6** | **Rate Limiting Login & Audit Logging** | **Selesai (100%)** | HTTP 429 pada 5x gagal berturut-turut & log bersih | Maruf Syahbana |
| **7** | **Security Headers & Cookie Flags** | **Selesai (100%)** | `tests/uji_cepat.py` memvalidasi `HttpOnly`, `SameSite`, dan headers | Maruf Syahbana |
| **8** | **Skrip Gladi Demo 5 Menit** | **Selesai (100%)** | `docs/skrip-demo.md` terstruktur 5 segmen terukur | Maruf Syahbana |
| **9** | **Skrip Uji Cepat Mandiri (`tests/uji_cepat.py`)** | **Selesai (100%)** | Output konsisten: `"SEMUA UJI LULUS"` | Maruf Syahbana |
