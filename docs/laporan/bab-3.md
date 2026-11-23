# BAB III PERANCANGAN SISTEM DAN RENCANA PENGUJIAN

Bab ini mendokumentasikan secara komprehensif seluruh proses analisis kebutuhan, pemodelan sistem berbasis UML, perancangan arsitektur basis data relasional ternormalisasi, desain antarmuka pengguna (wireframe), hasil tinjauan desain (*design review*), serta strategi dan rencana pengujian perangkat lunak untuk Sistem Manajemen Rental PlayStation (Exito Playbox).

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

### 3.2.3 Batasan Sistem (*Won't Have*)
1. **W-01 Pembayaran Digital Otomatis (*Payment Gateway API*):** Pembayaran sewa dilakukan secara tunai (*cash*) atau transfer perbankan manual langsung di meja kasir.
2. **W-02 Pelacakan Lokasi GPS Konsol:** Perangkat beroperasi secara tetap di dalam lokasi toko, sehingga modul pelacak GPS ditiadakan.
3. **W-03 Ekspor Laporan Berkas Eksternal (PDF/Excel):** Berdasarkan hasil konfirmasi dengan pemilik, laporan keuangan difokuskan tersaji langsung pada layar dasbor aplikasi.

---

## 3.3 Pemodelan Sistem Berbasis UML

Sistem dimodelkan menggunakan standar UML yang mencakup diagram use case, skenario alur use case, dan diagram aktivitas (*activity diagram*).

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

### 3.4.1 Hasil Konfirmasi Aturan Data dengan Klien
Pada sesi review aturan data bersama pemilik rental (Langkah 14), disepakati sejumlah aturan integritas fisik:
1. Akun kasir yang berhenti bekerja tidak boleh di-hard delete (cukup dinonaktifkan via kolom `is_active = 0`).
2. Unit konsol fisik yang rusak dialihkan statusnya ke `'maintenance'`, tanpa dihapus dari basis data.
3. Tarif sewa dikunci pada tabel paket resmi (`harga >= 0`) dan paket terikat pada jenis konsol tertentu (`jenis_konsol IN ('PS3', 'PS4', 'PS5')`).
4. Kasir wajib menginput nama pelanggan pada form transaksi sewa untuk menghindari kekeliruan unit saat ruang rental ramai.
5. Transaksi darurat (mati lampu $< 5$ menit pertama) dapat dibatalkan dengan status `'batal'`.
6. Riwayat transaksi disimpan permanen (*No Hard Delete*) minimal 3–5 tahun untuk keperluan audit keuangan.

### 3.4.2 Struktur Tabel Ternormalisasi (3NF)
Basis data diimplementasikan pada **SQLite** dengan penegakan kunci asing (`PRAGMA foreign_keys = ON`), terdiri atas 5 entitas:
1. **`users`** (`id` [PK], `username` [UNIQUE], `password_hash`, `role`, `is_active`).
2. **`consoles`** (`id` [PK], `kode_konsol` [UNIQUE], `jenis_konsol`, `status`).
3. **`packages`** (`id` [PK], `nama_paket` [UNIQUE], `jenis_konsol`, `durasi_menit`, `harga`, `is_active`).
4. **`transactions`** (`id` [PK], `nama_pelanggan`, `user_id` [FK], `console_id` [FK], `package_id` [FK], `waktu_mulai`, `waktu_selesai`, `status_bayar`).
5. **`fines`** (`id` [PK], `transaction_id` [FK, UNIQUE], `menit_terlambat`, `biaya_denda`).

---

## 3.5 Perancangan Antarmuka Pengguna (User Interface)

### 3.5.1 Peta Navigasi Sistem
Peta navigasi (`docs/desain/wireframe/navigasi.png`) mengadopsi struktur terpusat di mana seluruh 7 halaman fungsional dapat diakses dalam maksimal 1 hingga 2 kali klik dari Dasbor Utama. Halaman Laporan Omset dan Kelola Master diberi penanda khusus pemilik untuk menegakkan prinsip pembatasan hak akses (*Role-Based Access Control*).

### 3.5.2 Daftar Halaman Wireframe dan Fungsi
1. **`wf-01-login`:** Formulir otentikasi kasir dan pemilik dengan penanganan pesan galat kredensial salah / akun nonaktif.
2. **`wf-02-dasbor-utama` (Beranda):** Tampilan grid kartu konsol dengan indikator status Hijau (`Tersedia`), Merah (`Terpakai`), Kuning (`Overtime`), dan Abu-abu (`Maintenance`), dilengkapi countdown timer dan status polling 10 detik.
3. **`wf-03-buka-sewa`:** Formulir transaksi pembukaan sewa dengan kunci unit konsol terpilih, input nama pelanggan, dropdown paket resmi per tipe unit, dan radio metode pembayaran.
4. **`wf-04-selesai-sewa-denda`:** Halaman penutupan sewa kasir yang menampilkan rincian durasi terpakai, alert deteksi *overtime* di atas 5 menit, kalkulasi denda otomatis, dan tombol pembatalan sewa darurat.
5. **`wf-05-kelola-master` (Khusus Pemilik):** Tabel pengelolaan unit konsol (toggle status pemeliharaan) dan tabel paket sewa (toggle aktif/arsip).
6. **`wf-06-riwayat-transaksi`:** Tabel audit trail transaksi dengan filter pencarian nama pelanggan dan paginasi data.
7. **`wf-07-laporan-pendapatan` (Khusus Pemilik):** Dasbor keuangan yang menyajikan filter periode, tiga kartu metrik omset (sewa, denda, total bersih), serta rincian kontribusi omset per unit konsol PlayStation.

### 3.5.3 Penerapan Prinsip Desain dan Evaluasi Tinjauan (*Design Review*)
- **Pencegahan Galat (*Error Prevention*):** Kasir tidak dapat mengetik durasi atau harga sewa secara manual; input digantikan oleh dropdown paket sewa resmi. Aksi pembatalan transaksi pada `wf-04` diproteksi oleh dialog konfirmasi (*confirmation modal*) untuk menghindari salah klik.
- **Umpan Balik Segera (*Immediate Feedback*):** Status unit yang mengalami keterlambatan sewa memicu perubahan warna kartu menjadi kuning disertai efek visual berkedip (*pulsing border*) dan notifikasi audio browser singkat.
- **Konsistensi (*Consistency*):** Seluruh halaman mengadopsi navigasi atas (*top bar*) identik dengan warna tema `#0F172A` dan penataan tombol aksi yang seragam.

---

## 3.6 Rencana Pengujian dan Matriks Keterlacakan

### 3.6.1 Strategi Pengujian
Pengujian memadukan teknik *Manual Black-Box Testing* (Equivalence Partitioning dan Boundary Value Analysis), pengujian otomatis integritas skema SQLite, serta sesi *User Acceptance Testing* (UAT) bersama pemilik rental. Kriteria kelulusan mensyaratkan 100% kasus uji *Must* dan minimal 85% kasus uji *Should* berstatus lulus (*Pass*).

### 3.6.2 Ringkasan Test Case Terukur
Sistem diverifikasi oleh 11 kasus uji (*test case*) utama yang mencakup kondisi normal, kasus tidak valid, dan nilai batas:
- **TC-01 & TC-02 (KF-01):** Verifikasi perubahan status konsol menjadi 'terpakai' dan penolakan sewa ganda pada konsol yang sedang aktif.
- **TC-03 & TC-04 (KF-02):** Pengujian nilai batas durasi minimum (30 menit) dan batas bawah harga paket promo (Rp 0).
- **TC-05 & TC-06 (KF-03):** Pengujian nilai batas keterlambatan tepat 5 menit (*grace period*, denda = Rp 0) dan 6 menit (melewati ambang batas, denda pertama Rp 2.000).
- **TC-07 (KF-04 / KNF-01):** Pengujian sinkronisasi dasbor visual via polling 10 detik dengan waktu muat $\le 2$ detik.
- **TC-08 (KF-06):** Verifikasi kalkulasi omset laporan harian di mana transaksi batal tidak terhitung ke pendapatan.
- **TC-09 (KF-08):** Penolakan penyimpanan data transaksi saat kolom nama pelanggan dikosongkan.
- **TC-10 (KF-07):** Ketepatan pemfilteran data riwayat transaksi berdasarkan nama pelanggan.
- **TC-11 (KNF-03):** Pemblokiran akses rute laporan keuangan bagi pengguna dengan peran kasir (HTTP 403 Forbidden).

### 3.6.3 Matriks Keterlacakan Komprehensif
Seluruh kebutuhan fungsional dan non-fungsional terpetakan secara utuh ke use case, halaman wireframe, prioritas MoSCoW, dan nomor kasus uji verifikasi (sebagaimana tertuang pada Tabel Matriks Keterlacakan di `docs/srs.md` dan `docs/pengujian/rencana-uji.md`), membuktikan bahwa tidak ada kebutuhan yang tertinggal (*untested*) dan tidak ada pengujian di luar ruang lingkup yang disepakati bersama klien.

---

## 3.7 Perubahan terhadap Rancangan Awal dan Sinkronisasi Pengujian

Selama proses implementasi pada Bab 4, terdapat sejumlah penyesuaian teknis terhadap rancangan awal yang tercantum pada Bab 3. Penyesuaian ini dipicu oleh hasil pengujian unit, temuan audit keamanan OWASP, penutupan laporan cacat melalui *Test-Driven Development* (TDD), serta optimalisasi beban server kasir. 

Tabel 3.5 merangkum seluruh perubahan arsitektural dan rancangan detail (Lampiran B.4).

**Tabel 3.5 Matriks Perubahan terhadap Rancangan Awal (Bab 3 vs Bab 4)**

| Komponen Rancangan | Rancangan Awal (Bab 3) | Realisasi Implementasi (Bab 4) | Alasan Perubahan | Kategori Perubahan |
| :--- | :--- | :--- | :--- | :---: |
| **Penamaan Kolom Kueri JOIN Transaksi** | Kueri SQL JOIN mengasumsikan kolom nama konsol adalah `c.nama_konsol`. | Disesuaikan menjadi `c.kode_konsol` sesuai kamus data skema basis data SQLite. | Menjaga konsistensi DDL SQLite dan mencegah kesalahan `sqlite3.OperationalError: no such column`. | **Perbaikan** |
| **Sanitasi Masukan Nama Pelanggan Transaksi** | Validasi masukan mengasumsikan tipe selalu teks: `nama_pelanggan.strip()`. | Normalisasi eksplisit via `str(nama_pelanggan).strip()` pada `_validate_transaction_payload()`. | Penutupan Cacat D-01: payload non-string (seperti integer via dev tools) sebelumnya memicu eksepsi 500 `AttributeError`. | **Penyempurnaan** |
| **Integritas Keunikan Nama Paket Sewa** | Batasan `UNIQUE(nama_paket)` standar SQLite yang bersifat *case-sensitive*. | Validasi kueri `LOWER(nama_paket) = LOWER(?)` sebelum operasi INSERT maupun UPDATE di `services.py`. | Penutupan Cacat D-02: mencegah data ganda akibat variasi huruf kapital (misal "Paket Malam" vs "paket malam"). | **Penyempurnaan** |
| **Proteksi Mutasi Status Konsol Terpakai** | Pemilik diperbolehkan mengubah status konsol secara manual ke `'maintenance'` kapan saja. | Penolakan mutasi manual (HTTP 400) bila konsol sedang berada dalam status `'terpakai'`. | Penutupan Cacat D-03: melindungi konsistensi status operasional konsol yang sedang disewa aktif oleh pelanggan. | **Perbaikan** |
| **Mekanisme Perlindungan CSRF** | Direncanakan menggunakan pustaka pihak ketiga `Flask-WTF`. | Membangun modul generator token CSRF internal berbasis sesi dan middleware `@app.before_request`. | Menghindari *dependency bloat*, memangkas jejak memori runner di mesin kasir, dan kontrol penuh atas pesan galat 400. | **Simplifikasi** |
| **Cakupan Rencana Pengujian (3.6 vs 4.4)** | Rencana pengujian awal memuat 11 kasus uji manual dasar (TC-01 s/d TC-11). | Realisasi mencakup 22 test case otomatis pytest (38 *passed*), 3 uji cacat TDD, uji alur HTTP, dan matriks RBAC. | Peningkatan rigor pengujian otomatis, jaminan regresi tanpa cacat, dan verifikasi batas masukan menggunakan fixture terisolasi. | **Penyempurnaan** |

Terkait sinkronisasi rencana pengujian, seluruh 11 kasus uji yang dirancang pada Subbab 3.6 telah terbukti tercakup secara penuh dalam pengujian otomatis di Subbab 4.4 (misalnya TC-01 dan TC-02 tercakup pada `test_crud_konsol.py` dan `test_alur_akses.py`; TC-05 dan TC-06 tercakup pada `test_validasi.py` dan `test_transaksi_berelasi.py`; TC-11 tercakup pada pengujian matriks RBAC). Penambahan 11 test case baru pada Subbab 4.4 dilakukan secara terencana untuk memvalidasi kasus uji batas ekstrem, kekebalan injeksi SQL berparameter, proteksi token CSRF, serta verifikasi penutupan 3 cacat perangkat lunak (D-01, D-02, D-03).

