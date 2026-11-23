# Salindia Presentasi Tugas Besar Rekayasa Perangkat Lunak
## Exito Playbox — PlayStation Rental Management System

---

### Slide 1: Judul dan Identitas Tim
- **Judul Proyek:** Sistem Manajemen Rental PlayStation Berbasis Web (Exito Playbox)
- **Mata Kuliah:** Praktikum Rekayasa Perangkat Lunak (Semester Genap 2025/2026)
- **Tim Pengembang:** Maruf Syahbana (NIM: 2024xx / Full-Stack & Scrum Master)
- **Mitra Usaha:** Exito Playbox Rental PS (Bpk. Hendra — Sampit, Kalteng)
- **Versi Rilis:** v1.0.1 (Production Ready)
- **Tautan Repositori:** https://github.com/marufsyahbana2005/rpl-project-ps

---

### Slide 2: Latar Belakang & Masalah Mitra
- **Karakteristik Usaha:** Rental 8 unit konsol (2 PS3, 4 PS4, 2 PS5) dengan sistem sewa paket jam operasional harian.
- **Poin Masalah Utama (*Pain Points*):**
  1. *Human Error* Pencatatan: Perhitungan jam sewa manual pada nota kertas rawan salah hitung saat kasir sibuk.
  2. Ketiadaan Visibilitas Inventaris: Status konsol kosong vs terpakai tidak terpantau secara terpusat di meja kasir.
  3. Perselisihan Denda Keterlambatan: Ketiadaan standar toleransi (*grace period*) denda memicu komplain pelanggan.
  4. Rekapitulasi Finansial Lambat: Pemilik harus merekap nota kertas berjam-jam setiap malam untuk laporan harian.

---

### Slide 3: Solusi Digital & Nilai Tambah Sistem
- **Solusi yang Dibangun:** Aplikasi web responsif khusus kasir dan pemilik rental yang terisolasi di jaringan lokal gerai.
- **Nilai Tambah Nyata:**
  - **Otomatisasi Siklus Transaksi:** Pembukaan sewa 1-klik, timer otomatis, dan penyelesaian transaksi terintegrasi kalkulasi denda.
  - **Integritas Multi-Tabel Atomik:** Perubahan status transaksi sewa dan ketersediaan unit konsol terikat dalam satu blok transaksi database tanpa risiko *race condition*.
  - **Dasbor Finansial Real-Time:** Pemilik dapat memantau pendapatan paket dan denda seketika dari peramban.

---

### Slide 4: Arsitektur Sistem & Struktur 3-Tier
- **Pola Arsitektur:** Arsitektur Tiga Lapis (*Three-Tier Architecture*):
  1. *Presentation Layer:* HTML5, CSS Kustom Responsif, Templat Jinja2 dengan *autoescape* proteksi XSS.
  2. *Application / Logic Layer:* Framework Python Flask 3.1.3 dengan pemisahan Controller (`app.py`) dan Service Layer (`services.py`).
  3. *Data Storage Layer:* SQLite 3 dengan penegakan integritas relasional penuh (`PRAGMA foreign_keys = ON`).
- **Pemisahan Peran (*RBAC*):** Dua peran pengguna terotentikasi: `kasir` (operasional sewa) dan `owner` (kelola master paket, konsol, & audit).

---

### Slide 5: Alur Kerja & Demo Fitur Utama Kasir
- **Alur Kerja Operasional Rental:**
  1. *Login Kasir:* Otentikasi aman dengan pembersihan sesi aktif.
  2. *Buka Sewa:* Dropdown konsol otomatis hanya memunculkan unit yang berstatus `tersedia`; pilihan paket resmi.
  3. *Pemantauan Sewa Aktif:* Indikator visual badge durasi dan peringatan bila melewati waktu paket.
  4. *Selesai Sewa & Denda:* Sistem menghitung keterlambatan secara otomatis (toleransi 5 menit gratis, denda Rp 1.000/menit), merilis konsol kembali ke `tersedia`, dan mencetak ringkasan struk.

---

### Slide 6: Pengerasan Keamanan Berbasis OWASP Top 10
- **Hasil Audit Keamanan Mandiri (7 Kerentanan SEC-PS-01 s/d SEC-PS-07 Diatasi):**
  - *A01 Broken Access Control:* Penegakan decorator otorisasi `@peran_diperlukan` di server; sanitasi anti-Open Redirect pada query `next`.
  - *A02 Cryptographic Failures:* Penggantian hash plaintext dengan KDF modern *scrypt* ber-salt acak unik.
  - *A03 Injection:* Penggunaan kueri SQL berparameter 100% dan sanitasi wildcard LIKE dengan klausul `ESCAPE '\'`.
  - *A05 Security Misconfiguration:* Cookie sesi `HttpOnly=True`, `SameSite=Lax`, dan penyuntikan security headers `X-Frame-Options: SAMEORIGIN` anti-Clickjacking.
  - *A07 Identification Failures:* Proteksi CSRF token di seluruh formulir mutasi data POST, pembatasan laju login (*Rate Limiting* 5x gagal / 5 menit), dan audit logging tanpa menyimpan kata sandi.

---

### Slide 7: Strategi Pengujian & Penutupan Cacat (TDD)
- **Statistik Pengujian Otomatis:**
  - 22 Kasus Uji Otomatis (38 skenario *passed* pada Pytest 9.1.1).
  - Skrip verifikasi cepat `tests/uji_cepat.py` lulus 100% dalam waktu $< 2$ detik.
  - Pengujian mutasi manual (*mutation testing*) membuktikan seluruh asersi uji sensitif terhadap perubahan operator batas.
- **Penutupan 3 Cacat Melalui Test-Driven Development (TDD):**
  - **D-01:** Normalisasi tipe masukan `str(nama_pelanggan)` mencegah *crash* HTTP 500 saat menerima payload non-string.
  - **D-02:** Validasi duplikasi nama paket sewa secara *case-insensitive* (`LOWER(nama_paket)`).
  - **D-03:** Proteksi penolakan mutasi status manual bagi konsol yang sedang disewa aktif.

---

### Slide 8: Hasil Validasi Pengguna (UAT) & Usabilitas SUS
- **Pelaksanaan UAT Bersama Mitra Rental:**
  - Responden: Bpk. Hendra (Pemilik) dan Rian Pratama (Operator Kasir).
  - 6 Skenario Operasional Riil (Login, Buka Sewa, Kelola Master, Perhitungan Denda, Filter Transaksi).
  - **Tingkat Kelulusan Skenario UAT: 100% Lulus (6 dari 6 skenario).**
- **Evaluasi Usability Menggunakan System Usability Scale (SUS):**
  - Skor SUS Rata-rata: **87.5 / 100**
  - Kategori Interpretasi: **Grade A+ (Kategori "Best Imaginable" / Sangat Memuaskan)**.
  - Responden menyatakan antarmuka sangat mudah dipelajari tanpa memerlukan pelatihan komputer yang rumit.

---

### Slide 9: Kesiapan Rilis & Arsitektur Deployment Produksi
- **Standar Rilis:** Mengadopsi *Semantic Versioning* (Tag `v1.0.0` dan Hotfix `v1.0.1`).
- **Runner Produksi WSGI Waitress:**
  - Tidak menggunakan development server Flask bawaan.
  - Dijalankan via `jalankan.py` memanfaatkan server *Waitress* multi-threaded (6 worker threads) yang stabil di Windows.
- **Pencadangan Online Tanpa Downtime:**
  - Utilitas `cadangkan.py` memanfaatkan SQLite Online Backup API.
  - Pencadangan konsisten tanpa perlu menghentikan transaksi rental aktif.
- **Dokumentasi Lengkap:** README komprehensif (lolos *Stranger Test*) dan Manual Pengguna non-teknis.

---

### Slide 10: Analisis Praktik Vibe Coding & Kolaborasi AI
- **Metrik Evaluasi Jurnal (Total 61 Entri Pengembangan):**
  - **Terima (Accepted):** 55 entri (**90.2%**) — Kode AI modular, rapi, dan lolos uji regresi.
  - **Ubah (Modified):** 6 entri (**9.8%**) — Intervensi manusia pada aspek keamanan kritis, validasi batas, dan konfigurasi server.
  - **Tolak (Rejected):** 0 entri (**0.0%**) — Efektivitas teknik *prompt engineering* berbasis DDL skema.
- **Karakteristik Galat AI:**
  - Galat keamanan dan logika membutuhkan waktu penanganan terpanjang (rata-rata 25 menit) karena bersifat senyap.
  - Verifikasi manusia (*human-in-the-loop*) mutlak diperlukan untuk mencegah kode yang "tampak berjalan" tetapi rapuh secara arsitektur.

---

### Slide 11: Keterbatasan Teknis & Rekomendasi Masa Depan
- **Keterbatasan Sistem Saat Ini:**
  1. Rate limiter berbasis in-memory (reset saat server restart; belum mendukung cluster).
  2. Pembayaran masih berbasis rekonsiliasi manual kasir (belum ada gateway QRIS otomatis).
  3. Pencadangan data masih tersimpan pada media penyimpanan lokal mesin kasir.
- **Rekomendasi Pengembangan Lanjutan:**
  1. Migrasi ke basis data terdistribusi PostgreSQL dan caching Redis untuk deployment multi-cabang.
  2. Integrasi webhook QRIS dinamis (Midtrans/Xendit) untuk auto-settlement transaksi sewa.
  3. Kontainerisasi aplikasi via Docker dan replikasi cadangan otomatis ke penyimpanan cloud terenkripsi.

---

### Slide 12: Kesimpulan
1. Sistem Exito Playbox berhasil dibangun sesuai target PRD, memenuhi 100% kebutuhan fungsional (KF-01 s/d KF-08) dan non-fungsional.
2. Keamanan sistem telah diperkeras memenuhi standar OWASP Top 10 dengan perlindungan CSRF, hashing ber-salt, RBAC ketat, dan cookie flags.
3. Pendekatan *Controlled Vibe Coding* terbukti mengakselerasi siklus pengembangan hingga 3x lipat dengan tetap menjaga integritas kualitas kode melalui disiplin pengujian otomatis TDD dan audit sejawat.
4. Sistem telah berada dalam status produksi aktif (v1.0.1) dan siap digunakan secara penuh oleh mitra usaha.

---

### Slide 13: Sesi Tanya Jawab (Q&A) & Penutup
- Terima kasih kepada dosen pengampu, asisten praktikum, dan mitra Exito Playbox.
- Sesi demonstrasi sistem dan tanya jawab dibuka.
- *Demonstrator: Maruf Syahbana.*
