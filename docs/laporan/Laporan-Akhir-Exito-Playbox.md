# LAPORAN AKHIR TUGAS BESAR REKAYASA PERANGKAT LUNAK
# SISTEM MANAJEMEN RENTAL PLAYSTATION BERBASIS WEB
## (EXITO PLAYBOX — `rpl-project-ps`)

- **Nama Pengembang:** Maruf Syahbana
- **Peran:** Product Owner, Scrum Master, & Full-Stack Developer
- **Mitra Usaha:** Exito Playbox Rental PS (Bpk. Hendra — Sampit, Kalimantan Tengah)
- **Status Rilis:** v1.0.1 (Production Ready)
- **Repositori:** https://github.com/marufsyahbana2005/rpl-project-ps

---

# BAB III PERANCANGAN SISTEM DAN RENCANA PENGUJIAN

Bab ini mendokumentasikan secara komprehensif seluruh proses analisis kebutuhan, pemodelan sistem berbasis UML, perancangan arsitektur basis data relasional ternormalisasi, desain antarmuka pengguna (wireframe), hasil tinjauan desain (*design review*), strategi pengujian perangkat lunak, serta matriks perubahan terhadap rancangan awal untuk Sistem Manajemen Rental PlayStation (Exito Playbox).

---

## 3.1 Gambaran Umum dan Konteks Pengembangan

### 3.1.1 Profil Klien dan Karakteristik Bisnis
Exito Playbox merupakan usaha jasa rental konsol permainan PlayStation yang beroperasi di Kota Sampit, Kotawaringin Timur. Tempat usaha ini dikelola langsung oleh pemilik (*Owner*), Bpk. Hendra, dengan dibantu oleh staf operator kasir. Unit konsol yang disewakan berjumlah 8 unit, terdiri atas 2 unit PlayStation 3 (PS3), 4 unit PlayStation 4 (PS4), dan 2 unit PlayStation 5 (PS5). Setiap unit dilengkapi dengan televisi dan perlengkapan stik nirkabel yang disewakan menggunakan skema paket jam (*hourly billing*).

### 3.1.2 Permasalahan Operasional
Berdasarkan hasil elisitasi kebutuhan dan wawancara lapangan pada Minggu 1–3, teridentifikasi sejumlah masalah utama operasional:
1. **Kesalahan Pencatatan Manual:** Kasir mencatat jam mulai sewa pada nota kertas. Ketika antrean pelanggan menumpuk di akhir pekan, kasir kerap keliru menghitung selisih waktu sewa dan total tagihan.
2. **Ketiadaan Visibilitas Ketersediaan Unit:** Kasir kesulitan memantau unit konsol mana yang kosong atau sedang berjalan tanpa harus memeriksa satu per satu ke setiap ruangan/layar TV.
3. **Perselisihan Denda Keterlambatan (*Overtime*):** Perhitungan denda kelebihan waktu sewa dilakukan secara perkiraan manual tanpa standar toleransi (*grace period*) yang pasti, sehingga memicu keluhan pelanggan.
4. **Ketiadaan Rekapitulasi Finansial Otomatis:** Pemilik harus menghitung ulang seluruh lembaran nota fisik setiap malam untuk mengetahui total omset harian dan performa unit rental terlaris.

### 3.1.3 Metode Pengembangan dan Alur *Vibe Coding* Terkendali
Pengembangan sistem Exito Playbox menerapkan metodologi **Agile Scrum** dengan durasi 4 sprint mingguan, mengedepankan pendekatan *vibe coding* terkendali (*Controlled Vibe Coding*). Dalam pendekatan ini:
- **Peran Manusia (Analyst & Developer):** Memegang kendali mutlak atas pendefinisian aturan bisnis, arsitektur data, verifikasi logika, dan persetujuan kode (*Review & Approve*).
- **Peran AI:** Digunakan sebagai akselerator perancangan draf awal, pembuatan skenario kasus uji (*test case*), dan pemodelan diagram berdasarkan batasan ketat dokumen PRD dan kamus data.
- **Integritas Versi (Git):** Setiap artefak dikelola melalui percabangan fitur Git yang terstruktur (`docs-antarmuka`, `docs-rencana-uji`) dengan tinjauan sejawat (*pull request*) sebelum digabungkan ke cabang utama (`main`).

---

## 3.2 Analisis Kebutuhan Sistem

### 3.2.1 Kebutuhan Fungsional (KF) dengan Prioritas MoSCoW
Kebutuhan fungsional diturunkan dari *User Story* (US-01 s/d US-03) dan diklasifikasikan menggunakan metode MoSCoW:

| ID KF | Deskripsi Kebutuhan Fungsional | Sumber | Prioritas | Test Case Terkait |
|:--:|---|:--:|:--:|:--:|
| **KF-01** | Mengubah status unit konsol menjadi 'terpakai' saat sewa dimulai dan kembali 'tersedia' saat selesai. | US-01 | **Must** | TC-01, TC-02 |
| **KF-02** | Mengalkulasi durasi dan total biaya sewa secara otomatis berdasarkan paket jam resmi yang dipilih. | US-01 | **Must** | TC-03, TC-04 |
| **KF-03** | Menghentikan timer dan menghitung denda keterlambatan secara otomatis berdasarkan aturan *grace period* 5 menit. | US-01 | **Should** | TC-05, TC-06 |
| **KF-04** | Menyajikan dasbor visual pemantauan status ketersediaan seluruh konsol secara *real-time* via *HTTP polling*. | US-02 | **Must** | TC-07 |
| **KF-05** | Menyediakan fitur penyaringan (*filter*) daftar unit konsol berdasarkan jenis konsol (PS3, PS4, PS5). | US-02 | Could | TC-Filt-01 |
| **KF-06** | Merekapitulasi total pendapatan transaksi sewa harian dan bulanan secara otomatis tanpa kalkulasi manual. | US-03 | **Must** | TC-08 |
| **KF-07** | Menyimpan riwayat transaksi sewa secara permanen dan menyediakan fitur penelusuran audit nota sewa. | US-03 | **Should** | TC-10 |
| **KF-08** | Memvalidasi kelengkapan masukan form kasir (nama pelanggan wajib diisi) sebelum data disimpan ke basis data. | US-01 | **Should** | TC-09 |
| **KF-09** | Mencatat inventaris aksesori pendukung konsol (stik cadangan, kabel HDMI). | Analisis | Could | TC-Inv-01 |
| **KF-10** | Menyediakan pencarian data transaksi berdasarkan rentang tanggal dan nama pelanggan. | Analisis | Rendah | TC-10 |

### 3.2.2 Kebutuhan Non-Fungsional (KNF)
| ID KNF | Kategori | Parameter Kualitas Terukur | Prioritas | Test Case |
|:--:|---|---|:--:|:--:|
| **KNF-01** | Kinerja (*Performance*) | Halaman dasbor status ketersediaan unit wajib dimuat dalam waktu $\le 2$ detik pada jaringan lokal rental. | **Must** | TC-07 |
| **KNF-02** | Keandalan (*Reliability*) | Pencadangan (*backup*) file basis data SQLite otomatis minimal sekali setiap hari untuk mencegah kehilangan riwayat sewa. | **Should** | TC-Back-01 |
| **KNF-03** | Keamanan (*Security*) | Pembatasan hak akses berbasis peran (*Role-Based Access Control*): menu laporan omset hanya dapat diakses oleh akun *Owner*. | **Must** | TC-11 |
| **KNF-04** | Kegunaan (*Usability*) | Antarmuka kasir dirancang intuitif sehingga dapat dioperasikan oleh kasir baru dengan waktu pengenalan $\le 15$ menit. | **Should** | UAT-Usab-01 |

---

## 3.3 Pemodelan Sistem Berbasis UML

### 3.3.1 Use Case Diagram
Diagram use case memetakan interaksi antara dua aktor utama: **Kasir / Operator** dan **Pemilik Rental (Owner)** terhadap sistem Exito Playbox.
- **Kasir:** Berinteraksi dengan UC-01 (Catat Transaksi Sewa), UC-02 (Kelola Penghentian dan Denda), dan UC-03 (Pantau Ketersediaan Unit).
- **Pemilik (Owner):** Mengakses seluruh fungsi kasir ditambah hak khusus pada UC-04 (Lihat Laporan Pendapatan) dan UC-05 (Telusuri Riwayat Transaksi).
- Relasi `<<include>>`: UC-01 mengikutsertakan UC-03 untuk memastikan konsol berstatus tersedia sebelum sewa dibuka, dan UC-02 mengikutsertakan kalkulasi durasi dari UC-01.

### 3.3.2 Skenario Use Case Utama
- **UC-01 (Catat Transaksi Sewa):** Kasir memilih unit kosong $\rightarrow$ input nama pelanggan $\rightarrow$ pilih paket durasi $\rightarrow$ sistem memvalidasi kelengkapan $\rightarrow$ status konsol berubah 'terpakai' dan timer mulai berjalan mundur.
- **UC-02 (Kelola Penghentian dan Denda):** Kasir memilih transaksi aktif $\rightarrow$ sistem mengevaluasi durasi terpakai terhadap paket $\rightarrow$ jika keterlambatan $> 5$ menit (*grace period* terlewati), denda dihitung proporsional per 15/30 menit $\rightarrow$ kasir menerima pembayaran $\rightarrow$ unit konsol kembali 'tersedia'.
- **UC-03 (Pantau Dasbor Unit):** Dasbor melakukan *HTTP polling* berkala setiap 10 detik ke server untuk menyajikan warna status unit secara akurat bagi seluruh operator.
- **UC-04 (Lihat Laporan Pendapatan):** Pemilik memilih filter periode tanggal $\rightarrow$ sistem mengagregasi total transaksi berstatus 'lunas' $\rightarrow$ layar menampilkan total omset paket, denda, omset bersih, dan kontribusi per unit PlayStation.
- **UC-05 (Telusuri Riwayat Transaksi):** Pemilik dan kasir menelusuri data audit transaksi berdasarkan nama pelanggan atau tanggal tertentu dengan paginasi terstruktur.

---

## 3.4 Perancangan Basis Data Relasional

Basis data diimplementasikan pada **SQLite** dengan penegakan kunci asing (`PRAGMA foreign_keys = ON`), terdiri atas 5 entitas ternormalisasi 3NF:
1. **`users`** (`id` [PK], `username` [UNIQUE], `password_hash`, `role`, `is_active`).
2. **`consoles`** (`id` [PK], `kode_konsol` [UNIQUE], `jenis_konsol`, `status`).
3. **`packages`** (`id` [PK], `nama_paket` [UNIQUE], `jenis_konsol`, `durasi_menit`, `harga`, `is_active`).
4. **`transactions`** (`id` [PK], `nama_pelanggan`, `user_id` [FK], `console_id` [FK], `package_id` [FK], `waktu_mulai`, `waktu_selesai`, `status_bayar`).
5. **`fines`** (`id` [PK], `transaction_id` [FK, UNIQUE], `menit_terlambat`, `biaya_denda`).

---

## 3.5 Perancangan Antarmuka Pengguna (User Interface)

Peta navigasi sistem mengadopsi struktur terpusat di mana seluruh 7 halaman fungsional dapat diakses dalam maksimal 1 hingga 2 kali klik dari Dasbor Utama. Halaman Laporan Omset dan Kelola Master diberi penanda khusus pemilik untuk menegakkan prinsip pembatasan hak akses (*Role-Based Access Control*).

---

## 3.6 Rencana Pengujian dan Matriks Keterlacakan

Pengujian memadukan teknik *Manual Black-Box Testing* (Equivalence Partitioning dan Boundary Value Analysis), pengujian otomatis integritas skema SQLite, serta sesi *User Acceptance Testing* (UAT) bersama pemilik rental. Sistem diverifikasi oleh 11 kasus uji dasar yang mencakup kondisi normal, kasus tidak valid, dan nilai batas (TC-01 hingga TC-11).

---

## 3.7 Perubahan terhadap Rancangan Awal dan Sinkronisasi Pengujian

Selama proses implementasi pada Bab 4, terdapat sejumlah penyesuaian teknis terhadap rancangan awal yang tercantum pada Bab 3. Penyesuaian ini dipicu oleh hasil pengujian unit, temuan audit keamanan OWASP, penutupan laporan cacat melalui *Test-Driven Development* (TDD), serta optimalisasi beban server kasir. 

Tabel 3.5 merangkum seluruh perubahan arsitektural dan rancangan detail (Lampiran B.4).

**Tabel 3.5 Matriks Perubahan terhadap Rancangan Awal (Bab 3 vs Bab 4)**

| Komponen Rancangan | Rancangan Awal (Bab 3) | Realisasi Implementasi (Bab 4) | Alasan Perubahan | Kategori Perubahan |
| :--- | :--- | :--- | :--- | :---: |
| **Penamaan Kolom Kueri JOIN Transaksi** | Kueri SQL JOIN mengasumsikan kolom nama konsol adalah `c.nama_konsol`. | Disesuaikan menjadi `c.kode_konsol` sesuai kamus data skema basis data SQLite. | Menjaga konsistensi DDL SQLite dan mencegah kesalahan `sqlite3.OperationalError: no such column`. | **Perbaikan** |
| **Sanitasi Masukan Nama Pelanggan Transaksi** | Validasi masukan mengasumsikan tipe selalu teks: `nama_pelanggan.strip()`. | Normalisasi eksplisit via `str(nama_pelanggan).strip()` pada `_validate_transaction_payload()`. | Penutupan Cacat D-01: payload non-string (seperti integer via dev tools) sebelumnya memicu eksepsi 500 `AttributeError`. | **Penyempurnaan** |
| **Integritas Keunikan Nama Paket Sewa** | Batasan `UNIQUE(nama_paket)` standar SQLite yang bersifat *case-sensitive*. | Validasi kueri `LOWER(nama_paket) = LOWER(?)` sebelum operasi INSERT maupun UPDATE di `services.py`. | Penutupan Cacat D-02: mencegah data ganda akibat variasi huruf kapital (misal "Paket Hemat" vs "paket hemat"). | **Penyempurnaan** |
| **Proteksi Mutasi Status Konsol Terpakai** | Pemilik diperbolehkan mengubah status konsol secara manual ke `'maintenance'` kapan saja. | Penolakan mutasi manual (HTTP 400) bila konsol sedang berada dalam status `'terpakai'`. | Penutupan Cacat D-03: melindungi konsistensi status operasional konsol yang sedang disewa aktif oleh pelanggan. | **Perbaikan** |
| **Mekanisme Perlindungan CSRF** | Direncanakan menggunakan pustaka pihak ketiga `Flask-WTF`. | Membangun modul generator token CSRF internal berbasis sesi dan middleware `@app.before_request`. | Menghindari *dependency bloat*, memangkas jejak memori runner di mesin kasir, dan kontrol penuh atas pesan galat 400. | **Simplifikasi** |
| **Cakupan Rencana Pengujian (3.6 vs 4.4)** | Rencana pengujian awal memuat 11 kasus uji manual dasar (TC-01 s/d TC-11). | Realisasi mencakup 22 test case otomatis pytest (38 *passed*), 3 uji cacat TDD, uji alur HTTP, dan matriks RBAC. | Peningkatan rigor pengujian otomatis, jaminan regresi tanpa cacat, dan verifikasi batas masukan menggunakan fixture terisolasi. | **Penyempurnaan** |

---

# BAB IV IMPLEMENTASI, PENGUJIAN, DAN EVALUASI

Bab ini menguraikan seluruh realisasi teknis pengembangan sistem Exito Playbox, evaluasi pengerasan keamanan OWASP Top 10, hasil pengujian perangkat lunak multi-level, arsitektur rilis dan deployment produksi, serta pembahasan kritis mengenai dampak praktik vibe coding.

---

## 4.1 Lingkungan Pengembangan dan Penerapan Etika AI

Sistem Exito Playbox dibangun dan diuji pada lingkungan perangkat keras dan perangkat lunak yang terisolasi untuk memastikan stabilitas dan reproduksibilitas.

**Tabel 4.1 Spesifikasi Perangkat Keras dan Perangkat Lunak Lingkungan Pengembangan**

| Komponen | Spesifikasi Lingkungan Pengembang | Spesifikasi Lingkungan Produksi (Target) |
| :--- | :--- | :--- |
| **Sistem Operasi** | Windows 11 Home 64-bit (Build 26100) | Windows 10/11 Pro / Ubuntu Linux 22.04 LTS |
| **Prosesor (CPU)** | Intel Core i5 / AMD Ryzen 5 (4 Cores / 8 Threads, 2.4 GHz) | Dual-Core 2.0 GHz atau lebih tinggi |
| **Memori Utama (RAM)** | 16 GB DDR4 | Minimal 4 GB (Rekomendasi 8 GB) |
| **Penyimpanan (Storage)**| 512 GB NVMe SSD | 120 GB SSD (Kebutuhan instalasi < 500 MB) |
| **Runtime Bahasa** | Python 3.12.x / 3.13.x (CPython 64-bit) | Python 3.10.x s/d 3.13.x |
| **Virtual Environment** | Python Virtual Environment (`.venv`) | Isolated `.venv` |
| **Manajer Versi (VCS)** | Git 2.40+ (Integrasi GitHub) | Git Runtime untuk penarikan rilis stabil |

**Tabel 4.2 Daftar Dependensi Pustaka Perangkat Lunak (`requirements.txt`)**

| Nama Paket | Versi Terkunci | Peran dan Fungsi dalam Sistem |
| :--- | :--- | :--- |
| **Flask** | `3.1.3` | Framework web mikro utama untuk perutean HTTP, manajemen sesi, dan perenderan Jinja2. |
| **Werkzeug** | `3.1.3` | Pustaka utilitas WSGI, fungsi hashing kata sandi (`scrypt`), dan penanganan payload HTTP. |
| **Jinja2** | `3.1.5` | Mesin templat antarmuka dengan fitur proteksi otomatis terhadap XSS (*autoescaping*). |
| **Waitress** | `3.0.2` | Server produksi WSGI multi-threaded murni (*pure-Python*) untuk deployment lingkungan kasir. |
| **pytest** | `9.1.1` (Dev) | Framework pengujian otomatis unit, integrasi, dan pengujian batas masukan parametris. |
| **pytest-cov** | `6.0.0` (Dev) | Perangkat pengukuran cakupan kode (*code coverage*) pengujian perangkat lunak. |

### Penerapan Etika Penggunaan Kecerdasan Buatan (AI)
Pengembangan sistem ini memanfaatkan kakas asisten kecerdasan buatan (*Generative AI*) berbasis model Gemini melalui lingkungan terpandu Antigravity. Seluruh tim memegang teguh prinsip etika akademik:
1. **Transparansi Log Aktivitas:** Setiap interaksi, saran kode, dan prompt terdokumentasi secara kronologis pada jurnal vibe coding.
2. **Kedaulatan Logika Manusia (*Human-in-the-Loop*):** AI bertindak sebagai akselerator penyusun draf kode dan skenario uji awal. Seluruh arsitektur, pemilihan dependensi, mitigasi celah keamanan, dan verifikasi kebenaran logika dikendalikan dan disetujui secara mutlak oleh pengembang manusia.
3. **Akuntabilitas Penuh:** Seluruh bug, regresi fungsional, maupun kegagalan keamanan menjadi tanggung jawab penuh pengembang manusia, bukan kesalahan entitas kecerdasan buatan.

---

## 4.2 Implementasi Fitur dan Siklus Rekayasa Prompt

Sistem Exito Playbox dibangun menggunakan **Arsitektur Tiga Lapis (*Three-Tier Architecture*)** yang memisahkan lapisan Presentasi (`templates/`), Lapisan Logika Bisnis (`services.py`), dan Lapisan Akses Data (`models.py`).

Tiga fitur utama yang menjadi tulang punggung sistem adalah:
1. **Fitur F1 — Manajemen Master Konsol (CRUD & Status Inventaris):** Mengelola unit konsol fisik dengan validasi ketat kode unik dan jenis konsol (PS3/PS4/PS5).
2. **Fitur F2 — Transaksi Buka Sewa Multi-Tabel Atomik:** Membuka sesi sewa kasir dengan memilih unit konsol yang sedang berstatus `'tersedia'` dan mengikatnya ke baris transaksi baru secara atomik.
3. **Fitur F3 — Penyelesaian Sewa & Perhitungan Denda Otomatis:** Menutup transaksi sewa dengan mengevaluasi durasi penggunaan nyata terhadap durasi paket; bila melewati toleransi 5 menit (*grace period*), denda Rp 1.000/menit dihitung otomatis dan dicatat ke tabel `fines`.

Berikut adalah implementasi transaksi atomik pada lapisan layanan data:

```python
# services.py: Transaksi atomik pembukaan sewa konsol
def create_transaction(nama_pelanggan, user_id, console_id, package_id):
    # Validasi payload masukan
    is_valid, msg = _validate_transaction_payload(nama_pelanggan, console_id, package_id)
    if not is_valid:
        return False, msg

    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Verifikasi ketersediaan konsol
        cursor.execute("SELECT status FROM consoles WHERE id = ?", (console_id,))
        row = cursor.fetchone()
        if not row or row["status"] != "tersedia":
            return False, "Konsol tidak tersedia untuk disewa."

        # Mutasi dua tabel dalam satu transaksi atomik
        cursor.execute(
            """INSERT INTO transactions (nama_pelanggan, user_id, console_id, package_id, waktu_mulai, status_bayar)
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 'lunas')""",
            (nama_pelanggan.strip(), user_id, console_id, package_id)
        )
        cursor.execute("UPDATE consoles SET status = 'terpakai' WHERE id = ?", (console_id,))
        conn.commit()
        return True, "Sesi sewa berhasil dibuka."
```

---

## 4.3 Tinjauan dan Pengerasan Keamanan (OWASP Top 10)

Berdasarkan hasil audit mandiri terhadap basis kode prototipe awal, teridentifikasi 7 potensi celah keamanan (SEC-PS-01 hingga SEC-PS-07) yang berhasil dimitigasi secara tuntas.

**Tabel 4.5 Matriks Temuan Audit Keamanan dan Status Perbaikan (OWASP Top 10)**

| ID Temuan | Kategori OWASP | Deskripsi Celah Keamanan | Tingkat Risiko | Status Perbaikan | Commit Git Terkait |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **SEC-PS-01** | A07:2021 Identification & Auth | Ketiadaan perlindungan CSRF pada 8 formulir mutasi POST. | **Tinggi** | **Tuntas Teratasi** | `7d828de` |
| **SEC-PS-02** | A07:2021 Identification & Auth | Kerentanan serangan brute-force login tanpa batas percobaan. | **Tinggi** | **Tuntas Teratasi** | `7d828de` |
| **SEC-PS-03** | A05:2021 Security Misconfig | Cookie sesi tidak memiliki atribut `HttpOnly`, `SameSite`, dan `Secure`. | Sedang | **Tuntas Teratasi** | `7d828de` |
| **SEC-PS-04** | A05:2021 Security Misconfig | Ketiadaan security headers (`X-Frame-Options`, `X-Content-Type`). | Sedang | **Tuntas Teratasi** | `7d828de` |
| **SEC-PS-05** | A02:2021 Cryptographic Failures | Penggunaan *hard-coded secret key* default pada mode produksi. | **Tinggi** | **Tuntas Teratasi** | `7d828de` |
| **SEC-PS-06** | A01:2021 Broken Access Control | Potensi Open Redirect pada manipulasi parameter query `next`. | Sedang | **Tuntas Teratasi** | `a46bae5` |
| **SEC-PS-07** | A03:2021 Injection | Penanganan karakter wildcard `%` dan `_` pada kueri pencarian LIKE. | Rendah | **Tuntas Teratasi** | `98fb5a8` |

---

## 4.4 Pengujian Perangkat Lunak dan Evaluasi Usabilitas

Pengujian sistem dilakukan melalui tiga lapisan: pengujian otomatis berbasis pytest, penutupan laporan cacat menggunakan *Test-Driven Development* (TDD), serta *User Acceptance Testing* (UAT) bersama mitra riil.

**Tabel 4.7 Ringkasan Eksekusi Pengujian Otomatis Pytest**

| Kategori Pengujian | Berkas Skrip Pengujian | Jumlah Test Case | Jumlah Skenario Uji | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Validasi & Batas** | `tests/test_validasi.py` | 5 | 13 skenario | **100% Lulus (Passed)** |
| **Alur & Akses RBAC**| `tests/test_alur_akses.py`| 5 | 9 skenario | **100% Lulus (Passed)** |
| **CRUD Konsol** | `tests/test_crud_konsol.py` | 4 | 5 skenario | **100% Lulus (Passed)** |
| **CRUD Paket** | `tests/test_crud_packages.py` | 3 | 4 skenario | **100% Lulus (Passed)** |
| **Transaksi Berelasi**| `tests/test_transaksi_berelasi.py`| 3 | 4 skenario | **100% Lulus (Passed)** |
| **Rilis & Cadangan** | `tests/test_rilis.py` | 2 | 3 skenario | **100% Lulus (Passed)** |
| **TOTAL** | **6 berkas pengujian** | **22 Test Case** | **38 Skenario** | **100% Passed (1.48 detik)** |

Tiga cacat perangkat lunak diselesaikan tuntas via TDD:
- **Cacat D-01:** Normalisasi `str(nama_pelanggan)` (commit `16db5e1`).
- **Cacat D-02:** Validasi duplikasi paket case-insensitive `LOWER(nama_paket)` (commit `f7f17d9`).
- **Cacat D-03:** Proteksi penolakan mutasi status konsol aktif (commit `60f2567`).

Pengujian UAT bersama Bpk. Hendra dan kasir rental menghasilkan tingkat kelulusan 100% pada 6 skenario operasional dan skor **System Usability Scale (SUS)** rata-rata sebesar **87.5 / 100 (Grade A+, Kategori Excellent)**.

---

## 4.5 Rilis dan Deployment Produksi

Sistem Exito Playbox dirilis mengikuti standar **Semantic Versioning** (`v1.0.0` dan perbaikan `v1.0.1`). Untuk lingkungan operasional toko, sistem dijalankan menggunakan runner produksi WSGI **Waitress** versi 3.0.2 dengan konfigurasi multi-threaded:

```bash
# Perintah eksekusi runner produksi Waitress pada mesin kasir
waitress-serve --listen=127.0.0.1:8000 --threads=6 app:app
```

Integritas data transaksi diamankan melalui skrip utilitas `cadangkan.py` yang memanfaatkan SQLite Online Backup API untuk mencadangkan basis data secara konsisten tanpa downtime (*zero-downtime hot backup*).

---

## 4.6 Pembahasan Kritis dan Analisis Vibe Coding

Sistem berhasil memenuhi 100% dari 8 Kebutuhan Fungsional (KF-01 s/d KF-08) dan 3 Kebutuhan Non-Fungsional (KNF-01 s/d KNF-03) dari PRD.

Berdasarkan ekstraksi kuantitatif terhadap 61 entri log jurnal vibe coding:
- **Terima (Accepted):** 55 entri (**90.2%**).
- **Ubah (Modified):** 6 entri (**9.8%**).
- **Tolak (Rejected):** 0 entri (**0.0%**).

Analisis dampak waktu membuktikan bahwa galat keamanan menuntut waktu perbaikan terpanjang (rata-rata 25 menit) akibat karakteristik *silent failure*. Praktik vibe coding berhasil meningkatkan kecepatan produksi kode, namun memindahkan beban kognitif pengembang manusia ke arah pengawasan arsitektur, pengujian mutasi, dan audit keamanan.

Tiga keterbatasan utama sistem saat ini adalah penyimpanan rate limiting berbasis in-memory, belum adanya integrasi payment gateway QRIS otomatis, dan pencadangan yang masih tersimpan lokal. Rekomendasi masa depan mencakup migrasi ke PostgreSQL/Redis, integrasi API QRIS dinamis, dan kontainerisasi aplikasi menggunakan Docker.

---

# DAFTAR PUSTAKA

[1] J. Brooke, "SUS: A 'Quick and Dirty' Usability Scale," in *Usability Evaluation in Industry*, P. W. Jordan, B. Thomas, I. L. McClelland, and B. Weerdmeester, Eds. London, UK: Taylor & Francis, 1996, pp. 189–194.

[2] OWASP Foundation, "OWASP Top 10: 2021 - The Ten Most Critical Web Application Security Risks," *OWASP Foundation*, 2021. [Online]. Tersedia: https://owasp.org/Top10/. [Diakses: 23-Mei-2026].

[3] T. Preston-Werner, "Semantic Versioning 2.0.0," *SemVer.org*, 2013. [Online]. Tersedia: https://semver.org/spec/v2.0.0.html. [Diakses: 23-Mei-2026].

[4] Pallets Projects, "Flask Documentation (Release 3.1.x)," *Pallets Projects*, 2024. [Online]. Tersedia: https://flask.palletsprojects.com/. [Diakses: 23-Mei-2026].

[5] Pallets Projects, "Werkzeug: The Comprehensive WSGI Web Application Library," *Pallets Projects*, 2024. [Online]. Tersedia: https://werkzeug.palletsprojects.com/. [Diakses: 23-Mei-2026].

[6] Pylons Project, "Waitress: Production-Quality Pure-Python WSGI Server," *Pylons Project Documentation*, 2024. [Online]. Tersedia: https://docs.pylonsproject.org/projects/waitress/en/latest/. [Diakses: 23-Mei-2026].

[7] D. R. Hipp, "SQLite: In-Process Database Engine & Online Backup API," *SQLite Consortium*, 2024. [Online]. Tersedia: https://www.sqlite.org/backup.html. [Diakses: 23-Mei-2026].

[8] H. Krekel et al., "pytest: Simple Powerful Testing with Python (Version 9.1.x)," *pytest.org*, 2025. [Online]. Tersedia: https://docs.pytest.org/. [Diakses: 23-Mei-2026].

[9] R. S. Pressman and B. R. Maxim, *Software Engineering: A Practitioner's Approach*, 9th ed. New York, NY, USA: McGraw-Hill Education, 2020.

[10] I. Sommerville, *Software Engineering*, 10th ed. Boston, MA, USA: Pearson, 2016.

[11] K. Beck, *Test-Driven Development: By Example*. Boston, MA, USA: Addison-Wesley Professional, 2002.

[12] National Institute of Standards and Technology (NIST), "Digital Identity Guidelines: Authentication and Lifecycle Management," *NIST Special Publication 800-63B*, 2020. [Online]. Tersedia: https://pages.nist.gov/800-63-3/sp800-63b.html. [Diakses: 23-Mei-2026].
