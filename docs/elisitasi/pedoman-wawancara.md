# Pedoman Wawancara - Sistem Manajemen Rental PlayStation

## A. Konteks

### 1. Masalah Utama Klien (Dugaan Awal)
- Pencatatan durasi dan tarif sewa unit konsol masih manual, sehingga rentan terjadi kesalahan perhitungan biaya sewa.
- Informasi ketersediaan konsol (PS3, PS4, PS5) belum terpantau secara *real-time*, menyulitkan saat ada pelanggan yang ingin *booking*.
- Laporan rekapitulasi keuangan dan penyewaan harian/bulanan belum terstruktur dengan baik.

### 2. Tabel Pemangku Kepentingan (Stakeholders)

| Pemangku Kepentingan | Peran | Kepentingan | Cara Dilibatkan |
|----------------------|-------|-------------|-----------------|
| Pemilik Rental (Owner) | Pengambil keputusan utama | Memantau rekapitulasi pendapatan, keamanan aset konsol, dan efisiensi operasional | Wawancara langsung & observasi |
| Kasir / Operator Rental | Pengguna harian sistem | Memproses transaksi sewa, input data penyewa, dan mengecek ketersediaan unit dengan cepat | Wawancara & uji coba (*usability test*) |
| Pelanggan / Penyewa | Pengguna akhir layanan | Mendapatkan kejelasan tarif, status ketersediaan unit konsol, dan proses penyewaan yang cepat | Observasi perilaku sewa |

### 3. Ruang Lingkup Proyek

**Hal yang Dikerjakan (In-Scope):**
- Manajemen data konsol dan status ketersediaan unit (*available*, *rented*, *maintenance*).
- Pencatatan transaksi penyewaan (durasi sewa, paket billing jam-jaman/harian) dan kalkulasi biaya otomatis.
- Modul rekapitulasi laporan pendapatan dan riwayat transaksi sewa harian/bulanan.

**Hal yang Sengaja Tidak Dikerjakan (Out-of-Scope):**
- Fitur integrasi *payment gateway* otomatis untuk pembayaran dompet digital (pembayaran tetap dilakukan secara tunai/transfer manual di tempat).
- Fitur pelacakan GPS fisik pada konsol yang dibawa pulang.

### 4. Batasan Proyek
- **Waktu:** Waktu penyelesaian hingga Minggu 16 semester berjalan.
- **Perangkat & Internet Klien:** Sistem dijalankan di komputer kasir rental dengan spesifikasi standar berbasis peramban (*web-based*), serta ketergantungan pada koneksi internet lokal/WiFi toko.
- **Kemampuan Pengguna:** Antarmuka harus dibuat sederhana dan intuitif agar kasir rental dapat mengoperasikannya tanpa pelatihan teknis yang rumit.
