# Skenario Use Case — Sistem Manajemen Rental PlayStation (Exito Playbox)

Dokumen ini mendeskripsikan rincian alur utama (*main flow*), alur alternatif, pengecualian, serta pascakondisi untuk setiap use case yang diturunkan dari kebutuhan fungsional (KF) pada dokumen SRS dan PRD.

---

## 1. UC-01 — Catat Transaksi Sewa
- **Aktor dan KF:** Kasir / Operator | KF-01, KF-02, KF-08
- **Prasyarat:** Kasir sudah masuk (*login*) ke dalam sistem dan berada di halaman utama pencatatan transaksi.
- **Alur Utama:**
  1. Kasir memilih unit konsol yang berstatus *Tersedia*.
  2. Kasir memilih paket durasi sewa yang diinginkan pelanggan.
  3. Sistem memvalidasi kelengkapan data masukan kasir.
  4. Kasir mengklik tombol "Mulai Sewa".
  5. Sistem mencatat waktu mulai, mengubah status unit konsol menjadi *Terpakai*, dan mengaktifkan timer durasi.
- **Alur Alternatif:**
  - 3a. Pelanggan memilih metode pembayaran tunai atau transfer manual; sistem langsung mencatat status pembayaran sebagai lunas atau *open bill*.
- **Pengecualian:**
  - 3b. Jika ada kolom data wajib yang kosong saat tombol simpan diklik, sistem menolak penyimpanan dan menampilkan pesan peringatan validasi input.
- **Pascakondisi:** Status unit konsol berubah menjadi *Terpakai* di database dan timer aktif berjalan.

---

## 2. UC-02 — Kelola Penghentian dan Denda
- **Aktor dan KF:** Kasir / Operator | KF-03
- **Prasyarat:** Sesi sewa konsol sedang berjalan dan timer aktif.
- **Alur Utama:**
  1. Kasir memilih transaksi sewa yang ingin dihentikan (*stop timer*).
  2. Sistem menghitung durasi total pemakaian dan membandingkannya dengan paket awal.
  3. Sistem menghentikan timer dan menghitung total biaya sewa akhir.
  4. Kasir mengonfirmasi penyelesaian transaksi.
  5. Sistem membebaskan unit konsol kembali ke status *Tersedia*.
- **Alur Alternatif:**
  - 2a. Durasi pemakaian sesuai persis dengan paket; tidak ada perhitungan biaya tambahan.
- **Pengecualian:**
  - 2b. Jika durasi sewa melebihi batas paket awal, sistem mendeteksi kelebihan waktu, menerapkan tarif denda proporsional (per kelipatan 30 menit), dan menambahkannya ke rincian total tagihan.
- **Pascakondisi:** Status unit konsol kembali *Tersedia* dan riwayat transaksi tercatat lengkap dengan rincian biaya denda.

---

## 3. UC-03 — Pantau Ketersediaan Unit
- **Aktor dan KF:** Kasir / Operator | KF-04
- **Prasyarat:** Kasir sudah masuk (*login*) ke dalam sistem aplikasi web.
- **Alur Utama:**
  1. Kasir membuka halaman dasbor utama aplikasi.
  2. Sistem mengambil data status terkini dari database melalui *HTTP polling* berkala.
  3. Sistem menampilkan daftar seluruh unit konsol (PS3, PS4, PS5) lengkap dengan indikator warna visual (Hijau = Kosong, Merah = Terpakai).
- **Alur Alternatif:**
  - 3a. Kasir menggunakan fitur penyaringan daftar unit berdasarkan jenis konsol tertentu.
- **Pengecualian:**
  - 3b. Jika koneksi basis data gagal dimuat, sistem menampilkan pesan galat (*error message*) dan tombol muat ulang (*refresh*).
- **Pascakondisi:** Dasbor menyajikan informasi visual ketersediaan unit konsol secara akurat dan *real-time*.

---

## 4. UC-04 — Lihat Laporan Pendapatan
- **Aktor dan KF:** Pemilik Rental (Owner) | KF-06
- **Prasyarat:** Pemilik rental sudah masuk (*login*) menggunakan akun berhak akses khusus (*owner*).
- **Alur Utama:**
  1. Pemilik memilih menu Laporan Pendapatan pada navigasi sistem.
  2. Pemilik memasukkan filter rentang tanggal (harian atau bulanan) yang ingin dilihat.
  3. Sistem mengalkulasi total omset transaksi pada rentang waktu tersebut secara otomatis.
  4. Sistem menyajikan ringkasan total pendapatan dan jumlah transaksi langsung di layar aplikasi.
- **Alur Alternatif:**
  - 2a. Pemilik memilih opsi *default* laporan hari ini; sistem langsung menampilkan rekapitulasi harian tanpa filter tambahan.
- **Pengecualian:**
  - 4a. Jika tidak ada transaksi pada rentang tanggal yang dipilih, sistem menampilkan informasi bahwa data laporan kosong untuk periode tersebut.
- **Pascakondisi:** Laporan pendapatan finansial tersaji secara transparan di layar pemilik rental tanpa kalkulasi manual.

---

## 5. UC-05 — Telusuri Riwayat Transaksi
- **Aktor dan KF:** Pemilik Rental (Owner) | KF-07
- **Prasyarat:** Pemilik rental sudah masuk (*login*) ke dalam sistem.
- **Alur Utama:**
  1. Pemilik membuka menu Riwayat Transaksi.
  2. Pemilik memasukkan kata kunci pencarian (misalnya tanggal transaksi atau nama penyewa).
  3. Sistem memindai basis data dan menampilkan tabel daftar riwayat transaksi yang cocok.
  4. Pemilik memilih salah satu baris transaksi untuk melihat detail lengkapnya.
- **Alur Alternatif:**
  - 3a. Pemilik menelusuri daftar riwayat secara berurutan berdasarkan halaman (*pagination*) tanpa kata kunci pencarian.
- **Pengecualian:**
  - 3b. Jika kata kunci pencarian tidak ditemukan di dalam basis data, sistem menampilkan pemberitahuan bahwa data riwayat tidak tersedia.
- **Pascakondisi:** Detail informasi riwayat transaksi masa lalu berhasil ditampilkan untuk keperluan audit atau verifikasi pemilik.
