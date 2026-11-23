# Laporan Temuan Keamanan Web & Audit Kode (Jobsheet 12) — Exito Playbox

- **Proyek:** Sistem Manajemen Rental PlayStation (Exito Playbox / `rpl-project-ps`)
- **Tanggal Audit:** 23 November 2026
- **Auditor:** Tim Pengembang Exito Playbox (Maruf Syahbana)
- **Acuan Standar:** OWASP Top 10: 2021

---

## 1. Peta OWASP & Prediksi Risiko Proyek

Tiga kategori OWASP yang paling relevan dan berisiko tinggi pada sistem rental PlayStation ini adalah:
1. **A01:2021 – Broken Access Control:** Pembatasan akses peran kasir vs pemilik, otorisasi transaksi multi-tabel, pencegahan manipulasi parameter (IDOR), dan proteksi CSRF.
2. **A07:2021 – Identification and Authentication Failures:** Keamanan kredensial, ketahanan login terhadap serangan *brute force*, dan manajemen sesi.
3. **A05:2021 – Security Misconfiguration:** Pengaturan kunci rahasia lingkungan, penonaktifan mode debug di lingkungan produksi, proteksi cookie sesi, dan penerapan Security HTTP Headers.

---

## 2. Tabel Analisis Kode Rentan (Kasus Latihan Lampiran B.1)

Tabel evaluasi 10 nomor kelemahan keamanan pada berkas kasus latihan:

| No | Masalah Keamanan | Kategori OWASP | Dampak Terhadap Sistem | Tingkat Risiko |
|:--:|---|:--:|---|:--:|
| **(1)** | `SECRET_KEY` diketik langsung (*hardcoded*) dan `debug=True` aktif tanpa pengaman lingkungan. | **A05:2021 – Security Misconfiguration** | Penyerang dapat memalsukan cookie sesi dan mengeksekusi kode sembarang (*Remote Code Execution*) via debugger interaktif. | **Kritis (Critical)** |
| **(2)** | Kueri SQL login menggunakan format string mentah (`f"SELECT ... WHERE user = '{u}'"`). | **A03:2021 – Injection** | Penyerang dapat melewati login tanpa kata sandi menggunakan manipulasi string SQL (`' OR '1'='1' --`). | **Kritis (Critical)** |
| **(3)** | Kata sandi disimpan tanpa garam (*salt*) atau hanya menggunakan algoritma cepat usang (`hashlib.md5`). | **A02:2021 – Cryptographic Failures** | Kata sandi mudah dibongkar massal menggunakan tabel pra-komputasi (*Rainbow Tables*) dan serangan kamus. | **Tinggi (High)** |
| **(4)** | Rute penghapusan data menggunakan metode `GET` tanpa pemeriksaan otentikasi/peran. | **A01:2021 – Broken Access Control** | Siapa pun dapat menghapus data penting hanya dengan mengeklik tautan atau otomatis terhapus oleh perayap web (*crawler*). | **Kritis (Critical)** |
| **(5)** | Tidak ada mekanisme perlindungan token Cross-Site Request Forgery (CSRF) pada form mutasi data. | **A01:2021 – Broken Access Control** | Pengguna yang terautentikasi dapat dijebak situs jahat untuk mengeksekusi transfer/mutasi data tanpa sadar. | **Tinggi (High)** |
| **(6)** | Pengalihan parameter `next` tidak divalidasi ke jalur internal (*Open Redirect*). | **A01:2021 – Broken Access Control** | Pengguna dapat dialihkan ke domain phishing berbahaya (`https://jahat.example`) setelah login berhasil. | **Sedang (Medium)** |
| **(7)** | Tidak ada pembatasan frekuensi percobaan login (*Rate Limiting* / Anti Brute Force). | **A07:2021 – Identification & Auth Failures** | Penyerang dapat menjalankan skrip otomatis untuk menebak ribuan kombinasi kata sandi tanpa terblokir. | **Tinggi (High)** |
| **(8)** | Aplikasi mencatat (*logging*) kata sandi teks polos ke terminal dan menampilkan jejak galat internal. | **A09:2021 – Security Logging & Monitoring** | Kredensial sensitif bocor ke berkas log server dan arsitektur internal terekspos kepada pengguna luar. | **Sedang (Medium)** |
| **(9)** | Cookie sesi tidak dikonfigurasikan dengan atribut `HttpOnly`, `SameSite`, dan `Secure`. | **A05:2021 – Security Misconfiguration** | Sesi rentan dicuri lewat skrip jahat XSS (`document.cookie`) atau disalahgunakan dalam konteks lintas domain. | **Sedang (Medium)** |
| **(10)** | Server tidak mengirimkan Security HTTP Headers dasar (`X-Frame-Options`, `X-Content-Type-Options`). | **A05:2021 – Security Misconfiguration** | Aplikasi rentan disusupi serangan pembajakan klik (*Clickjacking*) dan eksploitasi manipulasi tipe MIME. | **Rendah (Low)** |

---

## 3. Pembuktian Tiga Temuan (Langkah 4)

### Bukti 1: SQL Injection Bypass Login (Kategori A03:2021)
- **Langkah & Masukan:**
  Pada formulir login, kolom nama pengguna diisi payload manipulasi kutip dan penanda komentar SQL:
  ```text
  Nama Pengguna: admin' OR '1'='1' --
  Kata Sandi: sembarang
  ```
- **Hasil Nyata:**
  Kueri SQL yang dieksekusi di backend menjadi:
  `SELECT id, role FROM users WHERE username = 'admin' OR '1'='1' --' AND password = '...'`
  Klausa pemeriksaan kata sandi diabaikan oleh penanda komentar `--`. Aplikasi meloloskan penyerang masuk langsung sebagai pengguna pertama (administrator/owner) dengan status HTTP 302/200 tanpa mengetahui kata sandi asli.

### Bukti 2: Penghapusan Data Tanpa Otentikasi via Metode GET (Kategori A01:2021)
- **Langkah & Masukan:**
  Tanpa membuka sesi login, penyerang mengirim permintaan HTTP GET langsung dari bilah alamat browser atau perintah terminal:
  ```bash
  curl -i http://localhost:5000/consoles/1/hapus-raw
  ```
- **Hasil Nyata:**
  Server mengembalikan HTTP 302 dan menghapus baris data ID #1 dari basis data. Aksi destruktif terjadi tanpa verifikasi sesi pengguna, tanpa otorisasi peran, dan melanggar semantik HTTP (GET dilarang mengubah status data).

### Bukti 3: Open Redirect Phishing (Kategori A01:2021)
- **Langkah & Masukan:**
  Penyerang menyebarkan URL terpercaya yang dimanipulasi parameter pengalihannya:
  `http://localhost:5000/login?next=https://jahat.example/pencuri-akun`
  Korban memasukkan kredensial yang valid pada form login.
- **Hasil Nyata:**
  Server langsung menerbitkan header `Location: https://jahat.example/pencuri-akun`. Korban terlempar keluar dari situs resmi menuju domain pihak ketiga berbahaya yang siap mengeksploitasi data korban.

---

## 4. Laporan Lima Temuan Kasus Latihan Terpenting (Format Lampiran D.1)

### Temuan 1: SQL Injection pada Kueri Autentikasi
- **ID Temuan:** SEC-CASE-01
- **Lokasi Kode:** `kasus_rentan.py` (Fungsi `login()`, baris 42)
- **Kategori OWASP:** A03:2021 – Injection
- **Deskripsi:** Kueri login menggunakan string formatting langsung dari input pengguna `request.form['username']` tanpa SQL berparameter.
- **Bukti:** Input `admin' OR '1'='1' --` berhasil melewati login.
- **Dampak:** Pengambilalihan hak akses seluruh sistem oleh pihak tidak berwenang.
- **Tingkat Risiko:** Kritis (CVSS 9.8)
- **Tindakan Perbaikan:** Gunakan kueri SQL berparameter (`?`) dan verifikasi hash password menggunakan `check_password_hash()`.
- **Status:** Diperbaiki

### Temuan 2: Penghapusan Data via Metode GET Tanpa Otorisasi (IDOR)
- **ID Temuan:** SEC-CASE-02
- **Lokasi Kode:** `kasus_rentan.py` (Rute `/delete/<id>`, baris 68)
- **Kategori OWASP:** A01:2021 – Broken Access Control
- **Deskripsi:** Penghapusan data diizinkan via metode GET dan tidak memeriksa status login maupun peran pengguna.
- **Bukti:** Permintaan GET dari curl tanpa cookie berhasil menghapus data di database.
- **Dampak:** Kehilangan data inventaris secara permanen oleh pengguna anonim.
- **Tingkat Risiko:** Kritis (CVSS 9.1)
- **Tindakan Perbaikan:** Wajibkan metode `POST`, pasang decorator otorisasi `@peran_diperlukan('owner')`, dan tambahkan token CSRF.
- **Status:** Diperbaiki

### Temuan 3: Ketiadaan Pembatasan Percobaan Login (Brute Force)
- **ID Temuan:** SEC-CASE-03
- **Lokasi Kode:** `kasus_rentan.py` (Rute `/login`, baris 35)
- **Kategori OWASP:** A07:2021 – Identification and Authentication Failures
- **Deskripsi:** Form login tidak membatasi jumlah kegagalan percobaan autentikasi.
- **Bukti:** Skrip otomatis dapat mengirim 500 permintaan login per detik tanpa ada pemblokiran IP/akun.
- **Dampak:** Akun pengguna dapat ditebak menggunakan teknik serangan kamus (*dictionary attack*).
- **Tingkat Risiko:** Tinggi (CVSS 7.5)
- **Tindakan Perbaikan:** Terapkan pembatasan percobaan login (maksimal 5 kegagalan per 5 menit per kombinasi IP + username).
- **Status:** Diperbaiki

### Temuan 4: Ketiadaan Proteksi Cross-Site Request Forgery (CSRF)
- **ID Temuan:** SEC-CASE-04
- **Lokasi Kode:** `kasus_rentan.py` (Seluruh rute form POST)
- **Kategori OWASP:** A01:2021 – Broken Access Control
- **Deskripsi:** Formulir mutasi data tidak memverifikasi token anti-pemalsuan permintaan lintas situs.
- **Bukti:** Halaman HTML eksternal berhasil mengirimkan form tersembunyi ke server atas nama sesi aktif korban.
- **Dampak:** Penyerang dapat mengubah konfigurasi sistem menggunakan hak akses korban yang sedang login.
- **Tingkat Risiko:** Tinggi (CVSS 7.4)
- **Tindakan Perbaikan:** Terapkan validasi token CSRF acak berbasis sesi pada setiap permintaan mutasi POST.
- **Status:** Diperbaiki

### Temuan 5: Kunci Rahasia Bocor & Debug Mode Aktif
- **ID Temuan:** SEC-CASE-05
- **Lokasi Kode:** `kasus_rentan.py` (Baris 12 & 85)
- **Kategori OWASP:** A05:2021 – Security Misconfiguration
- **Deskripsi:** `SECRET_KEY` ditulis sebagai teks polos di kode sumber dan server dijalankan dengan `debug=True`.
- **Bukti:** Nilai secret key terbaca jelas di repositori Git; debugger pin aktif di browser saat terjadi exception.
- **Dampak:** Pemalsuan cookie sesi dan potensi eksekusi kode jarak jauh (RCE).
- **Tingkat Risiko:** Kritis (CVSS 9.0)
- **Tindakan Perbaikan:** Ambil `SECRET_KEY` dari environment variable; matikan mode debug di lingkungan produksi.
- **Status:** Diperbaiki

---

## 5. Tinjauan Mandiri Kode Proyek Sendiri (Exito Playbox / Langkah 7)

Hasil audit mendalam terhadap kode sumber proyek `rpl-project-ps` pada branch `fitur/perbaikan-keamanan`:

| ID Temuan | Komponen / Berkas | Kategori OWASP | Deskripsi Kerentanan | Risiko | Keputusan Triase | Tindakan / Rencana |
|:--:|---|:--:|---|:--:|:--:|---|
| **SEC-PS-01** | `app.py` & `templates/*.html` | **A01:2021 – Broken Access Control** | Formulir mutasi data POST (sewa, konsol, paket, login, logout) belum memverifikasi token CSRF tersembunyi. | **Tinggi** | **Diperbaiki Hari Ini** | Terapkan token CSRF aman berbasis sesi dan validasi otomatis pada middleware `before_request`. |
| **SEC-PS-02** | `app.py` (Rute `/login`) | **A07:2021 – Identification & Auth Failures** | Rute login belum memiliki pembatasan laju (*Rate Limiting*) kegagalan autentikasi per kombinasi IP + username. | **Tinggi** | **Diperbaiki Hari Ini** | Tambahkan rate limiter memori (maks 5x gagal / 5 menit, respon HTTP 429) dan audit logging tanpa mencatat kata sandi. |
| **SEC-PS-03** | `app.py` (Konfigurasi Sesi) | **A05:2021 – Security Misconfiguration** | Cookie sesi belum mengonfigurasikan atribut keamanan `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE`, dan `SESSION_COOKIE_SECURE`. | **Sedang** | **Diperbaiki Hari Ini** | Aktifkan `HTTPONLY=True`, `SAMESITE='Lax'`, dan `SECURE` kondisional pada environment produksi. |
| **SEC-PS-04** | `app.py` (Middleware Respons) | **A05:2021 – Security Misconfiguration** | Header keamanan peramban (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`) belum disuntikkan pada respons HTTP. | **Sedang** | **Diperbaiki Hari Ini** | Tambahkan decorator `@app.after_request` untuk menyuntikkan ketiga security header esensial. |
| **SEC-PS-05** | `app.py` (Inisialisasi Kunci) | **A05:2021 – Security Misconfiguration** | Aplikasi masih menyediakan fallback string kunci rahasia pengembangan jika environment variable `SECRET_KEY` kosong di produksi. | **Sedang** | **Diperbaiki Hari Ini** | Tolak startup aplikasi (`RuntimeError`) bila dijalankan pada `FLASK_ENV=production` tanpa `SECRET_KEY` terkonfigurasi. |
| **SEC-PS-06** | `app.py` (Manajemen Sesi Idle) | **A07:2021 – Identification & Auth Failures** | Sesi pengguna belum memiliki waktu kedaluwarsa otomatis (*Session Idle Timeout* 30 menit). | **Rendah** | **Ditunda (Sprint 3)** | Dijadwalkan pada Sprint 3 bersama modul pemantauan aktivitas kasir real-time. |
| **SEC-PS-07** | `requirements.txt` | **A06:2021 – Vulnerable & Outdated Components** | Audit dependensi pustaka pihak ketiga belum diverifikasi menggunakan perkakas pemindai CVE otomatis. | **Rendah** | **Ditunda (Sprint 3)** | Dijadwalkan integrasi CI/CD audit menggunakan `pip-audit` pada Sprint 3. |
