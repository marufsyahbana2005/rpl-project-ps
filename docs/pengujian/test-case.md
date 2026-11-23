# Dokumen Test Case dan Matriks Keterlacakan — Exito Playbox (Jobsheet 13)

Dokumen ini memuat matriks keterlacakan kebutuhan (*Requirements Traceability Matrix*) dan rancangan $\ge 20$ skenario *test case* menggunakan teknik Partisi Ekuivalen (*Equivalence Partitioning*) dan Analisis Nilai Batas (*Boundary Value Analysis* / BVA), untuk sistem manajemen rental PlayStation **Exito Playbox** (`rpl-project-ps`).

---

## 1. Matriks Keterlacakan Kebutuhan (Lampiran B.1)

Tabel berikut memetakan setiap Kebutuhan Fungsional (KF) yang telah terimplementasi pada prototipe ke kriteria penerimaan dan ID *test case* pengujiannya.

| ID Kebutuhan | Nama Kebutuhan | Kriteria Penerimaan (Acceptance Criteria) | ID Test Case Terkait | Status Implementasi |
|:---:|---|---|:---:|:---:|
| **KF-01** | Pengelolaan Unit Konsol & Status Inventaris | Unit konsol tersimpan dengan kode unik ($\ge 4$ char), jenis valid (PS3/PS4/PS5), berstatus awal 'tersedia'. Status berubah atomik menjadi 'terpakai' saat sewa aktif, dan pulih 'tersedia' saat sewa selesai. | `TC-BVA-07`, `TC-BVA-08`, `TC-NEG-03`, `TC-NEG-05`, `TC-NORM-01`, `TC-NORM-02` | **Selesai (100%)** |
| **KF-02** | Kalkulasi Durasi & Tarif Paket Sewa | Durasi sewa harus berupa angka bulat $>0$ menit. Harga sewa harus $\ge 0$ (harga 0 untuk paket promo diperbolehkan; harga negatif ditolak). | `TC-BVA-01`, `TC-BVA-02`, `TC-BVA-03`, `TC-BVA-04`, `TC-NORM-02` | **Selesai (100%)** |
| **KF-03** | Penghentian Sewa & Perhitungan Denda | Selesai sewa menghentikan status aktif. Toleransi keterlambatan 5 menit (denda Rp 0). Melebihi 5 menit dikenakan denda Rp 1.000 per menit kelebihan, tercatat di tabel `fines`. | `TC-BVA-05`, `TC-BVA-06`, `TC-NORM-03` | **Selesai (100%)** |
| **KF-04** | Dasbor Monitoring Status Real-time | Dasbor menampilkan seluruh unit konsol dengan badge status warna (hijau: tersedia, merah: terpakai, kuning: maintenance) dan tabel transaksi aktif. | `TC-NORM-04` | **Selesai (100%)** |
| **KF-05** | Pencarian & Penyaringan Transaksi | Transaksi dapat dicari berdasarkan nama pelanggan (LIKE berparameter) dan difilter berdasarkan status bayar atau jenis konsol. | `TC-NORM-04` | **Selesai (100%)** |
| **KF-07** | Penyimpanan Riwayat Transaksi | Riwayat transaksi sewa tersimpan permanen di database dengan relasi lengkap ke data konsol, paket sewa, kasir, dan denda. | `TC-NORM-02`, `TC-NORM-03` | **Selesai (100%)** |
| **KF-08** | Validasi Masukan Form & Integritas Data | Form menolak input kosong, karakter tidak valid, format numerik salah, atau data duplikat secara ramah tanpa crash aplikasi. | `TC-NEG-01`, `TC-NEG-02`, `TC-NEG-04`, `TC-NEG-06` | **Selesai (100%)** |
| **KNF-03** | Otorisasi Hak Akses (RBAC) & Keamanan | Tamu diarahkan ke login, kasir ditolak HTTP 403 saat akses rute pemilik, form POST tanpa CSRF ditolak HTTP 400, dan brute-force login ditolak HTTP 429. | `TC-NEG-07`, `TC-NEG-08`, `TC-NEG-09`, `TC-NEG-10` | **Selesai (100%)** |

---

## 2. Perancangan Partisi Ekuivalen dan Nilai Batas

### 2.1 Isian 1: Harga Paket Sewa (`harga`)
- **Aturan Bisnis:** Integer $\ge 0$ (nilai 0 diizinkan untuk paket promosi gratis; nilai negatif dilarang).
- **Partisi Ekuivalen:**
  - *Valid:* Integer $\ge 0$ (Contoh: 0, 5000, 25000)
  - *Invalid Negatif:* Integer $< 0$ (Contoh: -1, -10000)
  - *Invalid Tipe Data:* String huruf, kosong, atau desimal cacat (Contoh: "gratis", "")
- **Nilai Batas (BVA):**
  - Batas Bawah: `-1` (Invalid), `0` (Valid batas bawah), `1` (Valid)

### 2.2 Isian 2: Durasi Paket Sewa (`durasi_menit`)
- **Aturan Bisnis:** Integer $> 0$ (durasi rental harus minimal 1 menit bulat).
- **Partisi Ekuivalen:**
  - *Valid:* Integer $\ge 1$ (Contoh: 1, 60, 120)
  - *Invalid Nol & Negatif:* Integer $\le 0$ (Contoh: 0, -1, -30)
  - *Invalid Tipe Data:* String kosong, teks alfabet (Contoh: "sejam", "")
- **Nilai Batas (BVA):**
  - Batas Bawah: `-1` (Invalid), `0` (Invalid batas), `1` (Valid batas bawah)

### 2.3 Isian 3: Toleransi Keterlambatan Pengembalian Sewa (`selisih_menit`)
- **Aturan Bisnis:** Batas toleransi keterlambatan adalah 5 menit (denda = Rp 0). Menit ke-6 dan seterusnya dikenakan denda Rp 1.000 / menit.
- **Partisi Ekuivalen:**
  - *Tepat Waktu / Dalam Toleransi:* Keterlambatan $\le 5$ menit $\rightarrow$ Denda Rp 0.
  - *Terlambat Kena Denda:* Keterlambatan $\ge 6$ menit $\rightarrow$ Denda = $(menit - 5) \times 1.000$.
- **Nilai Batas (BVA):**
  - Nilai Batas: `4 menit` (Denda Rp 0), `5 menit` (Batas maksimum toleransi, Denda Rp 0), `6 menit` (Batas pertama kena denda, Denda Rp 1.000).

### 2.4 Isian 4: Panjang Karakter Kode Unit Konsol (`kode_konsol`)
- **Aturan Bisnis:** String minimal 4 karakter (format standar misal `PS4-01`, `PS5-02`).
- **Partisi Ekuivalen:**
  - *Valid:* Panjang $\ge 4$ karakter.
  - *Invalid:* Panjang $< 4$ karakter.
- **Nilai Batas (BVA):**
  - Batas Bawah: `3 karakter` (Invalid batas atas), `4 karakter` (Valid batas bawah).

---

## 3. Tabel Rancangan Test Case (Lampiran B.2)

Komposisi 22 Test Case:
- **Nilai Batas (BVA):** 8 Kasus (`TC-BVA-01` s/d `TC-BVA-08`)
- **Uji Pelanggaran / Negatif:** 10 Kasus (`TC-NEG-01` s/d `TC-NEG-10`)
- **Jalur Normal (Happy Path):** 4 Kasus (`TC-NORM-01` s/d `TC-NORM-04`)

| ID Test Case | Kebutuhan Terkait | Teknik Uji | Deskripsi Skenario Pengujian | Masukan / Aksi Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|:---:|:---:|---|---|---|:---:|:---:|
| `TC-BVA-01` | **KF-02** | Nilai Batas | Tambah paket sewa dengan harga batas bawah = 0 (paket promo) | `harga = "0"`, `durasi = 60` | Paket berhasil disimpan, harga Rp 0, tanpa galat | Tersimpan sukses | **LULUS** |
| `TC-BVA-02` | **KF-02** | Nilai Batas | Tambah paket sewa dengan harga di bawah batas (-1) | `harga = "-1"`, `durasi = 60` | Ditolak: "Harga sewa tidak boleh bernilai negatif." | Ditolak dengan pesan valid | **LULUS** |
| `TC-BVA-03` | **KF-02** | Nilai Batas | Tambah paket sewa dengan durasi batas invalid = 0 menit | `durasi = "0"`, `harga = 10000` | Ditolak: "Durasi sewa harus lebih besar dari 0 menit." | Ditolak dengan pesan valid | **LULUS** |
| `TC-BVA-04` | **KF-02** | Nilai Batas | Tambah paket sewa dengan durasi batas bawah valid = 1 menit | `durasi = "1"`, `harga = 1000` | Paket berhasil disimpan dengan durasi 1 menit | Tersimpan sukses | **LULUS** |
| `TC-BVA-05` | **KF-03** | Nilai Batas | Selesai sewa terlambat pas batas toleransi 5 menit | Selesai sewa saat `selisih = 5 menit` | Transaksi lunas, denda = Rp 0, unit konsol 'tersedia' | Denda Rp 0, unit kembali | **LULUS** |
| `TC-BVA-06` | **KF-03** | Nilai Batas | Selesai sewa terlambat 6 menit (batas pertama kena denda) | Selesai sewa saat `selisih = 6 menit` | Transaksi lunas, denda = Rp 1.000, tercatat di `fines` | Denda Rp 1.000 tercatat | **LULUS** |
| `TC-BVA-07` | **KF-01** | Nilai Batas | Tambah konsol dengan kode panjang 3 karakter (< 4) | `kode_konsol = "PS4"`, `jenis = "PS4"` | Ditolak: "Kode konsol minimal 4 karakter." | Ditolak dengan pesan valid | **LULUS** |
| `TC-BVA-08` | **KF-01** | Nilai Batas | Tambah konsol dengan kode pas panjang minimal 4 karakter | `kode_konsol = "PS41"`, `jenis = "PS4"` | Konsol berhasil disimpan, status 'tersedia' | Tersimpan sukses | **LULUS** |
| `TC-NEG-01` | **KF-08** | Pelanggaran | Tambah konsol dengan kode kosong | `kode_konsol = ""`, `jenis = "PS4"` | Ditolak: "Kode konsol wajib diisi." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-02` | **KF-08** | Pelanggaran | Tambah konsol dengan jenis konsol dilarang | `kode_konsol = "XB-01"`, `jenis = "XBOX"` | Ditolak: "Jenis konsol tidak valid. Pilih PS3, PS4, atau PS5." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-03` | **KF-01** | Pelanggaran | Tambah konsol dengan kode yang sudah ada (duplikat UNIQUE) | `kode_konsol = "PS4-01"` (sudah ada) | Ditolak: "Kode konsol 'PS4-01' sudah terdaftar." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-04` | **KF-08** | Pelanggaran | Buka sewa tanpa memilih unit konsol | `console_id = ""`, `package_id = 1` | Ditolak: "Unit konsol wajib dipilih." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-05` | **KF-01** | Pelanggaran | Buka sewa dengan unit konsol yang sedang 'terpakai' | `console_id = 1` (sedang sewa aktif) | Ditolak: "Unit konsol tidak sedang tersedia untuk disewa." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-06` | **KF-08** | Pelanggaran | Buka sewa dengan nama pelanggan kosong | `nama_pelanggan = ""`, unit valid | Ditolak: "Nama pelanggan wajib diisi." | Ditolak dengan pesan valid | **LULUS** |
| `TC-NEG-07` | **KNF-03** | Pelanggaran | Kasir mengakses rute khusus owner `/consoles/tambah` | GET `/consoles/tambah` sesi kasir | Mengembalikan status HTTP 403 Forbidden | HTTP 403 Forbidden | **LULUS** |
| `TC-NEG-08` | **KNF-03** | Pelanggaran | Kasir mengirim POST hapus unit konsol | POST `/consoles/1/hapus` sesi kasir | Mengembalikan HTTP 403, data konsol tetap utuh | HTTP 403 Forbidden, utuh | **LULUS** |
| `TC-NEG-09` | **KNF-03** | Pelanggaran | Kirim permintaan POST tanpa token CSRF | POST `/login` tanpa field `csrf_token` | Mengembalikan status HTTP 400 Bad Request (CSRF Failure) | HTTP 400 Bad Request | **LULUS** |
| `TC-NEG-10` | **KNF-03** | Pelanggaran | Percobaan login gagal 6 kali berturut-turut | POST `/login` 6x password salah | Percobaan ke-6 ditolak status HTTP 429 Too Many Requests | HTTP 429 Too Many Requests | **LULUS** |
| `TC-NORM-01` | **KF-01** | Jalur Normal | Owner menambah unit konsol valid | `kode_konsol = "PS5-88"`, `jenis = "PS5"` | Data tersimpan di basis data dengan status 'tersedia' | Tersimpan berstatus 'tersedia' | **LULUS** |
| `TC-NORM-02` | **KF-01, 02**| Jalur Normal | Kasir membuka sesi sewa baru valid | `console_id = valid`, `package_id = valid` | Sesi sewa 'open_bill' tersimpan, unit otomatis 'terpakai' | Sewa tercatat, unit 'terpakai' | **LULUS** |
| `TC-NORM-03` | **KF-03, 07**| Jalur Normal | Kasir menyelesaikan sewa tepat waktu | POST `/sewa/<id>/selesai` tepat waktu | Transaksi 'lunas', unit konsol pulih 'tersedia', denda Rp 0 | Transaksi lunas, unit pulih | **LULUS** |
| `TC-NORM-04` | **KF-04, 05**| Jalur Normal | Dasbor menampilkan daftar transaksi & filter | Akses rute `/sewa?status_bayar=lunas` | Menampilkan transaksi yang berstatus lunas | Data terfilter akurat | **LULUS** |

---

## 4. Ringkasan Ketercakupan Pengujian
- **Total Test Case:** 22 Kasus
- **Jumlah Nilai Batas:** 8 Kasus ($\ge 6$ terpenuhi)
- **Jumlah Uji Pelanggaran / Negatif:** 10 Kasus ($\ge 6$ terpenuhi)
- **Jumlah Jalur Normal:** 4 Kasus ($\ge 3$ terpenuhi)
- **Ketercakupan Kebutuhan Fungsional:** 100% (Seluruh KF-01, KF-02, KF-03, KF-04, KF-05, KF-07, KF-08, dan KNF-03 terwakili).
