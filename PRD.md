# Product Requirements Document (PRD) — Sistem Manajemen Rental PlayStation (Exito Playbox)

## 1. Ringkasan Produk dan Tujuan
Exito Playbox Management System adalah aplikasi berbasis web menggunakan Python Flask dan SQLite yang dirancang untuk mengotomatisasi pencatatan transaksi sewa konsol, pemantauan status unit secara real-time via *polling* berkala, dan rekapitulasi laporan pendapatan harian. Tujuan utama produk ini adalah memangkas kesalahan pencatatan manual, mempercepat proses layanan kasir, serta memberikan transparansi finansial bagi pemilik rental.

## 2. Pengguna dan Peran
- **Kasir / Operator Rental:**
  - Memulai dan menghentikan sesi timer sewa konsol.
  - Memilih paket billing dan memproses pembayaran transaksi.
  - Memantau dasbor status ketersediaan unit konsol secara langsung.
- **Pemilik Rental (Owner):**
  - Mengakses rekapitulasi laporan pendapatan harian dan bulanan.
  - Meninjau riwayat transaksi penyewaan lengkap dengan pembatasan hak akses (*role-based restriction*).

## 3. Fitur per Prioritas (Must & Should Have)

### Fitur 1: Pencatatan Transaksi & Timer Sewa (Prioritas: Must)
- **Deskripsi:** Sistem mengelola siklus hidup sewa konsol dari mulai hingga selesai secara otomatis.
- **Kriteria Penerimaan (Given-When-Then):**
  - **Given** konsol dalam status *Tersedia*, **When** kasir memilih paket jam dan mengklik *Mulai Sewa*, **Then** status konsol berubah menjadi *Terpakai* dan timer durasi berjalan.
  - **Given** transaksi sewa sedang berjalan, **When** waktu habis atau penghentian diproses, **Then** sistem menghitung total biaya sesuai tarif dan membebaskan status konsol.

### Fitur 2: Dasbor Monitoring Ketersediaan Unit (Prioritas: Must)
- **Deskripsi:** Menampilkan kondisi seluruh unit konsol (PS3, PS4, PS5) dalam tampilan visual yang diperbarui secara berkala (*HTTP polling*).
- **Kriteria Penerimaan (Given-When-Then):**
  - **Given** pengguna berada di halaman dasbor utama, **When** halaman dimuat, **Then** sistem menampilkan seluruh unit konsol beserta indikator warna statusnya (Hijau = Kosong, Merah = Terpakai).

### Fitur 3: Rekapitulasi Laporan Pendapatan (Prioritas: Must)
- **Deskripsi:** Menyajikan laporan keuangan harian dan bulanan secara otomatis tanpa kalkulasi manual.
- **Kriteria Penerimaan (Given-When-Then):**
  - **Given** pemilik membuka halaman Laporan, **When** memilih filter tanggal harian, **Then** sistem menampilkan total pendapatan, jumlah transaksi, dan ringkasan penyewaan per unit.

### Fitur 4: Perhitungan Denda / Kelebihan Waktu Otomatis (Prioritas: Should)
- **Deskripsi:** Menghitung biaya tambahan secara otomatis apabila durasi sewa melebihi batas paket (dengan aturan pembulatan kelebihan waktu per 30 menit).
- **Kriteria Penerimaan (Given-When-Then):**
  - **Given** masa sewa telah melewati batas durasi paket, **When** transaksi dihentikan, **Then** sistem mendeteksi kelebihan waktu, menerapkan tarif denda proporsional, dan menambahkannya ke total tagihan.

### Fitur 5: Validasi Input & Riwayat Transaksi (Prioritas: Should)
- **Deskripsi:** Memastikan kelengkapan data masukan kasir dan menyimpan riwayat transaksi secara aman.
- **Kriteria Penerimaan (Given-When-Then):**
  - **Given** kasir membuat transaksi baru, **When** ada kolom wajib yang kosong lalu disimpan, **Then** sistem menolak penyimpanan dan menampilkan pesan peringatan validasi.

## 4. Data Awal (Entitas Utama dan Atribut Penting)
- **Unit Konsol:** id_konsol, 
ama_unit, jenis_konsol (PS3/PS4/PS5), status_unit (Tersedia/Terpakai/Maintenance).
- **Transaksi:** id_transaksi, id_konsol, waktu_mulai, waktu_selesai, durasi, 	otal_biaya, status_pembayaran.
- **Pengguna / Kasir:** id_user, 
ama_lengkap, username, password_hash, ole (Admin/Kasir).

## 5. Di Luar Lingkup (Won't Have & Could Have)
- **Integrasi Payment Gateway Otomatis (Won't Have):** Pembayaran digital otomatis melalui API pihak ketiga ditiadakan untuk rilis saat ini; pembayaran dilakukan secara tunai atau transfer manual di tempat.
- **Pelacakan GPS Fisik Konsol (Won't Have):** Fitur pelacakan perangkat secara langsung tidak disertakan karena unit dioperasikan di dalam area rental.
- **Filter Jenis Konsol & Manajemen Aksesori (Could Have):** Fitur lanjutan penyaringan unit dan pencatatan inventaris aksesori diposisikan sebagai opsi tambahan bila waktu pengembangan mencukupi.

## 6. Pertanyaan Terbuka untuk Klien
- Apakah aturan pembulatan denda kelebihan waktu disepakati dihitung per 30 menit atau per 1 jam penuh?
- Apakah laporan keuangan bulanan memerlukan fitur ekspor langsung ke format berkas Excel atau PDF?
