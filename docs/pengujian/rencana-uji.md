# Rencana Pengujian Perangkat Lunak (Test Plan) — Exito Playbox

Dokumen ini memuat strategi pengujian perangkat lunak, daftar kasus uji (*test case*) terperinci yang diturunkan dari kebutuhan PRD dan kamus data, catatan evaluasi bantuan AI, serta matriks keterlacakan kebutuhan terhadap pengujian.

---

## 1. Strategi Rencana Pengujian (Langkah 7)

### 1.1 Tujuan
Tujuan dari rencana pengujian ini adalah memastikan bahwa seluruh kebutuhan fungsional inti (terutama prioritas *Must* dan *Should*) pada sistem manajemen rental Exito Playbox berfungsi secara benar, akurat, dan aman. Pengujian ini berfokus pada:
1. Keandalan pencatatan waktu mulai, hitung durasi, dan penghentian timer sewa konsol.
2. Ketepatan kalkulasi biaya paket dan denda keterlambatan (*overtime*) sesuai aturan toleransi *grace period*.
3. Sinkronisasi status ketersediaan konsol secara *real-time* melalui dasbor kasir.
4. Keamanan hak akses pengguna (pembatasan menu laporan dan konfigurasi khusus pemilik).
5. Pencegahan masuknya data kosong atau tidak valid (*error prevention*).

### 1.2 Ruang Lingkup
- **Dalam Lingkup (In-Scope):**
  - Kebutuhan Fungsional Prioritas *Must*: KF-01 (Ubah status konsol), KF-02 (Kalkulasi durasi/biaya paket), KF-04 (Monitoring dasbor real-time), KF-06 (Rekapitulasi omset laporan harian).
  - Kebutuhan Fungsional Prioritas *Should*: KF-03 (Logika denda dan toleransi keterlambatan), KF-07 (Penyimpanan dan penelusuran riwayat), KF-08 (Validasi input kasir).
  - Kebutuhan Non-Fungsional: KNF-01 (Kinerja respon dasbor $\le 2$ detik) dan KNF-03 (Otorisasi hak akses peran *owner*).
- **Di Luar Lingkup (Out-of-Scope / Won't Have):**
  - W-01 Integrasi pembayaran otomatis pihak ketiga (*payment gateway API*).
  - W-02 Pelacakan fisik unit konsol via GPS.
  - Ekspor dokumen berkas PDF/Excel eksternal (laporan difokuskan tampil langsung pada layar aplikasi).

### 1.3 Strategi dan Pendekatan Pengujian
Pengujian dilaksanakan dengan kombinasi 3 pendekatan:
1. **Uji Fungsional Manual (*Manual Black-Box Testing*):**
   - Menguji antarmuka pengguna (UI) melalui peramban web (*browser*) dengan metode *Equivalence Partitioning* dan *Boundary Value Analysis*.
   - Menguji alur use case positif (*happy path*), skenario alternatif, dan alur pengecualian (*exception handling*).
2. **Uji Otomatis Tingkat Unit (*Unit & Database Constraint Testing*):**
   - Skrip Python untuk menguji logika kalkulasi denda keterlambatan dan kepatuhan batasan basis data SQLite (penegakan *Foreign Key*, nilai unik username/kode konsol, dan batasan *CHECK* harga non-negatif).
3. **Uji Keberterimaan Pengguna (*User Acceptance Testing* / UAT):**
   - Sesi validasi langsung bersama pemilik dan kasir rental Exito Playbox untuk memverifikasi kesesuaian sistem dengan alur operasional di lapangan.

### 1.4 Lingkungan Pengujian (*Test Environment*)
- **Perangkat Keras:** Laptop/PC penguji (Processor multi-core, RAM 8GB/16GB).
- **Sistem Operasi:** Windows 11 Home / Pro 64-bit.
- **Perangkat Lunak:** Python 3.10+, Flask 3.x, SQLite 3, Web Browser Google Chrome (versi terbaru) dan Microsoft Edge.
- **Data Uji (*Mock Test Data*):**
  - Akun Pengguna: 1 akun *Owner* aktif (`owner_hendra`), 1 akun *Kasir* aktif (`kasir_andi`), 1 akun kasir nonaktif (`kasir_lama`).
  - Unit Konsol: 8 unit fisik (PS3-01, PS3-02 [Maintenance], PS4-01, PS4-02, PS4-03, PS5-01, PS5-02, PS5-03).
  - Paket Sewa: Paket Reguler PS3 (Rp 8.000/jam), Paket Reguler PS4 (Rp 12.000/jam), Paket Reguler PS5 (Rp 20.000/jam), dan Paket Promo Bonus (Rp 0/jam).

### 1.5 Kriteria Lulus (*Pass/Fail Criteria*)
- **Kriteria Lulus (Pass):**
  - 100% *test case* prioritas *Must* (KF-01, KF-02, KF-04, KF-06) berstatus **LULUS (PASS)**.
  - Minimal 85% *test case* prioritas *Should* berstatus **LULUS (PASS)**.
  - Tidak ditemukan cacat kritis (*Critical / Blocker Bug*) yang menyebabkan sistem *crash*, basis data korup, atau salah kalkulasi uang kasir.
  - Otorisasi hak akses berhasil mencegah kasir membuka halaman laporan keuangan.
- **Kriteria Gagal (Fail):**
  - Terdapat kegagalan pada salah satu *test case* prioritas *Must*.
  - Terjadi kesalahan hitung omset atau manipulasi status konsol ganda (*double booking* pada unit yang sama).

### 1.6 Pembagian Tugas Penguji
| Nama Anggota | Peran | Tanggung Jawab Pengujian |
|---|---|---|
| **Maruf Syahbana** | Product Owner & Lead Developer | Penyusunan skenario uji, eksekusi uji otomatis unit/skema, pengujian *black-box* fungsi form kasir, dasbor, dan laporan. |
| **Bpk. Hendra / Operator Exito Playbox** | Klien / End-User | Pelaksana skenario UAT harian (pencatatan sewa langsung di kasir, verifikasi nota denda, dan pengecekan rekap omset). |

---

## 2. Daftar Test Case (Langkah 8)

Daftar *test case* di bawah ini disusun dari kriteria penerimaan PRD dan aturan kamus data, mencakup kebutuhan *Must* dan *Should*, serta dilengkapi minimal 2 kasus tidak valid dan 2 kasus nilai batas (*boundary value*).

| ID TC | Mengacu KF | Prasyarat & Data Uji | Langkah Pengujian | Hasil yang Diharapkan (Terukur) | Teknik Pengujian |
|:--:|:--:|---|---|---|:--:|
| **TC-01** | **KF-01** | - Kasir sudah login.<br>- Unit `PS4-01` status: `'tersedia'`.<br>- Data: Nama = `"Budi"`, Paket = `"Paket PS4 1 Jam"`. | 1. Buka dasbor `wf-02`.<br>2. Klik tombol `Mulai Sewa` pada unit `PS4-01`.<br>3. Isi nama `"Budi"`, pilih paket.<br>4. Klik `Mulai Sewa`. | Status konsol `PS4-01` di database dan dasbor berubah menjadi `'terpakai'`, timer mulai berjalan dari durasi 60:00 mundur, warna indikator berubah menjadi Merah. | Partisi Ekuivalen (Valid) |
| **TC-02** | **KF-01** | - Kasir sudah login.<br>- Unit `PS4-02` status: `'terpakai'`. | 1. Buka dasbor `wf-02`.<br>2. Periksa kartu unit `PS4-02`.<br>3. Coba kirim request sewa baru ke unit tersebut. | Tombol `Mulai Sewa` pada unit berstatus terpakai tidak tersedia (diganti tombol `Selesaikan`). Request sewa ganda ditolak sistem dengan pesan galat: `"Unit sedang terpakai"`. | Partisi Ekuivalen (**Kasus Tidak Valid 1**) |
| **TC-03** | **KF-02** | - Kasir membuka form sewa `wf-03`.<br>- Data paket terendah: Durasi batas minimum 30 menit, harga = Rp 8.000. | 1. Pilih unit `PS3-01`.<br>2. Pilih paket `"PS3 Singkat 30 Menit"`.<br>3. Simpan transaksi sewa. | Sistem mengalkulasi total tagihan sewa tepat bernilai Rp 8.000 dan waktu selesai dihitung tepat 30 menit dari waktu mulai. | Nilai Batas (**Nilai Batas 1: Durasi Minimum**) |
| **TC-04** | **KF-02** | - Kasir membuka form sewa `wf-03`.<br>- Data paket promo: Durasi 60 menit, harga = Rp 0 (nilai batas bawah non-negatif). | 1. Pilih unit `PS4-01`.<br>2. Pilih paket promo `"Bonus Turnamen 1 Jam"`.<br>3. Simpan transaksi sewa. | Transaksi tersimpan sukses; nilai tagihan paket tepat Rp 0 tanpa pesan error validasi harga; status bayar otomatis `'lunas'`. | Nilai Batas (**Nilai Batas 2: Batas Bawah Harga Non-Negatif**) |
| **TC-05** | **KF-03** | - Transaksi `PS5-01` berjalan.<br>- Paket durasi: 60 menit.<br>- Waktu pemakaian real: 65 menit (tepat pada ambang batas *grace period* 5 menit). | 1. Kasir membuka form selesai sewa `wf-04`.<br>2. Sistem membaca selisih waktu = 65 menit.<br>3. Kasir klik selesai. | Kolom `fines.menit_terlambat = 5`. Karena $\le 5$ menit (masih dalam grace period), sistem menghitung denda = Rp 0. Total tagihan tetap tarif paket asli (Rp 20.000). | Nilai Batas (**Nilai Batas 3: Tepat di Ambang Grace Period**) |
| **TC-06** | **KF-03** | - Transaksi `PS5-01` berjalan.<br>- Paket durasi: 60 menit.<br>- Waktu pemakaian real: 66 menit (1 menit melebihi batas *grace period*). | 1. Kasir membuka form selesai sewa `wf-04`.<br>2. Sistem mengevaluasi keterlambatan = 6 menit.<br>3. Kasir meninjau kalkulasi denda. | `fines.menit_terlambat = 6`. Sistem mendeteksi ambang grace period terlewati dan menerapkan denda kelipatan 15 menit pertama sebesar tepat Rp 2.000. Total tagihan = Rp 22.000. | Nilai Batas (**Nilai Batas 4: 1 Menit Melewati Ambang Batas**) |
| **TC-07** | **KF-04** | - Kasir A dan Kasir B membuka dasbor `wf-02` di browser terpisah.<br>- Unit `PS4-01` status awal: `'tersedia'`. | 1. Kasir A menyewa unit `PS4-01`.<br>2. Kasir B mengamati layar dasbornya tanpa memencet tombol reload manual. | Dalam kurun waktu maksimal 10 detik (*HTTP polling cycle*), indikator unit `PS4-01` pada layar Kasir B otomatis berubah warna menjadi Merah (`'terpakai'`). | Partisi Ekuivalen (Valid) |
| **TC-08** | **KF-06** | - Basis data memuat 3 transaksi hari ini:<br>TRX-1: Rp 24.000 (Lunas), TRX-2: Rp 20.000 (Lunas), TRX-3: Rp 12.000 (Batal). | 1. Pemilik membuka halaman laporan `wf-07`.<br>2. Pilih filter tanggal hari ini.<br>3. Klik `Tampilkan`. | Kartu metrik omset menampilkan angka tepat Rp 44.000 (TRX-3 yang berstatus batal tidak dihitung ke omset pendapatan). Jumlah transaksi terhitung: 2 transaksi. | Partisi Ekuivalen (Valid) |
| **TC-09** | **KF-08** | - Kasir berada di form buka sewa `wf-03`.<br>- Data: Kolom nama pelanggan dikosongkan (panjang karakter 0 / string kosong `""`). | 1. Pilih konsol `PS4-01`.<br>2. Kosongkan isian nama.<br>3. Klik tombol `Mulai Sewa`. | Sistem menolak pengiriman form, data tidak tersimpan ke database, dan muncul notifikasi peringatan: `"[!] Validasi Gagal: Nama pelanggan wajib diisi minimal 2 karakter!"`. | Partisi Ekuivalen (**Kasus Tidak Valid 2**) |
| **TC-10** | **KF-07** | - Basis data memiliki transaksi atas nama `"Budi Santoso"` dan `"Doni"`. | 1. Buka halaman riwayat `wf-06`.<br>2. Ketik kata kunci `"Budi"` pada kotak pencarian.<br>3. Klik `Cari Data`. | Tabel hanya menampilkan baris transaksi yang memuat nama `"Budi Santoso"`, baris pelanggan lain disembunyikan. | Partisi Ekuivalen (Valid) |
| **TC-11** | **KNF-03** | - Pengguna login menggunakan akun dengan peran kasir (`kasir_andi`). | 1. Kasir mencoba mengakses URL rute laporan keuangan `/laporan`. | Sistem memblokir akses rute, mengembalikan kode status HTTP 403 Forbidden, dan menampilkan pesan peringatan: `"Akses Ditolak: Anda tidak memiliki izin melihat laporan keuangan."`. | Pengujian Keamanan & Otorisasi |

---

### Catatan Evaluasi & Temuan Kesalahan AI (Hasil Review Penguji)
> **Catatan Kesalahan AI yang Ditemukan:**  
> Pada draf awal perancangan test case kalkulasi denda (KF-03), AI mengusulkan skenario di mana *"setiap keterlambatan 1 detik langsung memotong deposit saldo digital pelanggan secara otomatis melalui integrasi Payment Gateway"*.  
> **Koreksi Manusia:**  
> Test case tersebut salah dan bertentangan dengan PRD serta hasil konfirmasi aturan data klien. Pertama, sistem rental Exito Playbox tidak menggunakan payment gateway digital (masuk kategori *Won't Have* W-01). Kedua, klien telah menyepakati aturan toleransi keterlambatan (*grace period*) selama 5 menit pertama gratis untuk memberi waktu penyewa menyimpan game (*save game*) dan mengembalikan stik. Test case telah diperbaiki menjadi **TC-05** (keterlambatan 5 menit = Rp 0) dan **TC-06** (keterlambatan 6 menit = kena denda kelipatan pertama).

---

## 3. Matriks Keterlacakan (Traceability Matrix) — Langkah 9

Matriks ini menghubungkan kebutuhan fungsional (KF), kebutuhan non-fungsional (KNF), use case, halaman antarmuka pengguna, tingkat prioritas MoSCoW, serta nomor kasus uji (*test case*) yang memverifikasinya.

| ID KF / KNF | Deskripsi Kebutuhan | Use Case | Halaman Wireframe | Prioritas | Test Case Verifikasi |
|:--:|---|:--:|:--:|:--:|:--:|
| **KF-01** | Pengubahan status unit konsol menjadi terpakai saat mulai sewa. | UC-01 | `wf-02` Dasbor Utama<br>`wf-03` Buka Sewa | **Must** | **TC-01, TC-02** |
| **KF-02** | Perhitungan durasi dan biaya sewa otomatis berbasis paket jam sewa. | UC-01 | `wf-03` Buka Sewa | **Must** | **TC-03, TC-04** |
| **KF-03** | Penghentian timer dan kalkulasi denda keterlambatan (*overtime*). | UC-02 | `wf-04` Selesai Sewa & Denda | **Should** | **TC-05, TC-06** |
| **KF-04** | Dasbor monitoring ketersediaan seluruh konsol real-time via polling. | UC-03 | `wf-02` Dasbor Utama | **Must** | **TC-07** |
| **KF-06** | Rekapitulasi laporan pendapatan harian dan bulanan secara otomatis. | UC-04 | `wf-07` Laporan Pendapatan | **Must** | **TC-08** |
| **KF-07** | Penyimpanan riwayat transaksi dan penelusuran audit nota sewa. | UC-05 | `wf-06` Riwayat Transaksi | **Should** | **TC-10** |
| **KF-08** | Validasi input kasir sebelum penyimpanan transaksi ke database. | UC-01 | `wf-03` Buka Sewa | **Should** | **TC-09** |
| **KNF-01** | Waktu respon pemuatan dasbor status ketersediaan unit $\le 2$ detik. | UC-03 | `wf-02` Dasbor Utama | **Must** | **TC-07** |
| **KNF-03** | Pembatasan hak akses laporan dan master data khusus peran *owner*. | UC-04 | `wf-05` Kelola Master<br>`wf-07` Laporan Pendapatan | **Must** | **TC-11** |

### Verifikasi Keterlacakan:
- Seluruh kebutuhan fungsional prioritas **Must** memiliki minimal 1 (bahkan 2) test case verifikasi terukur.
- Seluruh kebutuhan fungsional prioritas **Should** terpetakan secara lengkap ke test case terkait.
- Tidak ada kebutuhan fungsional tanpa pengujian, dan tidak ada test case yang berada di luar ruang lingkup kebutuhan dokumen PRD dan SRS.
