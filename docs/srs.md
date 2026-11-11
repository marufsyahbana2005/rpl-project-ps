# Software Requirements Specification (SRS) - Sistem Rental PlayStation

## 1. Pendahuluan
Dokumen Spesifikasi Kebutuhan Perangkat Lunak ini mendeskripsikan fungsionalitas, parameter kualitas, dan batasan prioritas sistem manajemen rental konsol Exito Playbox.

## 2. Deskripsi Umum
Sistem ini dirancang untuk mengelola data unit konsol, transaksi penyewaan berbasis waktu, manajemen anggota, serta rekapitulasi laporan pendapatan kasir dan pemilik.

## 3. Kebutuhan Fungsional

| ID | Pernyataan Kebutuhan | Sumber | Prioritas | Asumsi? | Hasil yang Diharapkan (Test Case) |
|----|----------------------|--------|-----------|---------|---------------------------------|
| KF-01 | Sistem harus mengubah status konsol menjadi terpakai saat transaksi sewa dimulai. | US-01 | Must | Tidak | Status unit konsol berubah dari tersedia menjadi terpakai pada sistem. |
| KF-02 | Sistem harus menghitung durasi dan biaya sewa secara otomatis berdasarkan paket jam yang dipilih. | US-01 | Must | Tidak | Total biaya sewa muncul akurat sesuai durasi penggunaan. |
| KF-03 | Sistem harus menghentikan timer aktif dan menghitung biaya denda atau kelebihan waktu secara otomatis. | US-01 | Should | Tidak | Muncul rincian biaya tambahan saat waktu sewa melebihi batas paket. |
| KF-04 | Sistem harus menampilkan dasbor visual status ketersediaan seluruh unit konsol secara real-time. | US-02 | Must | Tidak | Indikator warna unit (kosong/terpakai) langsung diperbarui di layar kasir. |
| KF-05 | Sistem harus menyaring daftar unit konsol berdasarkan jenis konsol (PS3, PS4, PS5). | US-02 | Could | Ya | Operator dapat memfilter unit konsol sesuai permintaan pelanggan. |
| KF-06 | Sistem harus merekapitulasi total pendapatan transaksi harian dan bulanan secara otomatis. | US-03 | Must | Tidak | Laporan total omset harian tersaji tanpa perlu hitung manual. |
| KF-07 | Sistem harus menyimpan data riwayat transaksi sewa lengkap dengan identitas penyewa. | US-03 | Should | Ya | Data transaksi tersimpan di database dan dapat ditelusuri kembali. |
| KF-08 | Sistem harus memvalidasi input data kasir sebelum transaksi sewa baru disimpan ke database. | US-01 | Should | Ya | Muncul peringatan jika ada kolom data wajib yang kosong. |
| KF-09 | Sistem harus mencatat pencatatan data inventaris aksesori pendukung seperti stik dan kabel. | Analisis | Could | Ya | Stok aksesori tambahan tercatat dan terpantau kondisinya. |
| KF-10 | Sistem harus menyediakan fitur pencarian data riwayat transaksi berdasarkan tanggal atau nama penyewa. | Analisis | Rendah | Ya | Data transaksi lama dapat ditemukan dengan cepat melalui kolom pencarian. |

## 4. Kebutuhan Non-Fungsional

| ID | Kategori | Pernyataan Terukur | Sumber | Prioritas |
|----|----------|--------------------|--------|-----------|
| KNF-01 | Kinerja | Halaman dasbor status unit harus terbuka dalam waktu kurang dari atau sama dengan 2 detik pada perangkat komputer kasir standar. | Catatan Wawancara No. 1 & Analisis | Must |
| KNF-02 | Keandalan | Sistem harus melakukan pencadangan (*backup*) basis data otomatis minimal sekali setiap hari untuk mencegah kehilangan data transaksi saat terjadi kendala teknis. | Catatan Wawancara Analisis (Mitigasi Risiko) | Should |
| KNF-03 | Keamanan | Akses ke menu rekapitulasi laporan keuangan dan pengaturan sistem dibatasi hanya untuk akun dengan peran pemilik (*owner*). | Catatan Wawancara No. 3 | Must |
| KNF-04 | Kegunaan (*Usability*) | Antarmuka kasir harus dapat dioperasikan dengan mudah dan dipahami oleh pegawai baru dalam waktu pelatihan maksimal 15 menit tanpa panduan teknis yang rumit. | Catatan Wawancara Analisis (Karakteristik Pengguna) | Should |

## 5. Batasan dan Fitur yang Tidak Dikerjakan (Won't Have)

### Alasan Penentuan Prioritas Utama (*Must*):
- **KF-01, KF-02, KF-04, KF-06, KNF-01, KNF-03:** Merupakan fondasi mutlak operasional rental (pencatatan transaksi, timer dasar, visibilitas unit, laporan omset, kecepatan akses, dan pengamanan data finansial). Jika butir-butir ini tidak ada, sistem tidak dapat berfungsi untuk menyelesaikan masalah inti klien.
- Proporsi kebutuhan *Must* dijaga pada kisaran 35% dari total seluruh kebutuhan (6 dari 14 butir), sehingga aman dan realistis diselesaikan dalam batas waktu 4 sprint hingga Minggu 16.

### Daftar Fitur yang Ditunda / Tidak Dikerjakan (*Won't Have*):
- **W-01 Integrasi *Payment Gateway* Otomatis:** Pembayaran digital otomatis (QRIS dinamis / *e-wallet API*) ditiadakan karena keterbatasan waktu pengembangan hingga Minggu 16; transaksi pembayaran difokuskan secara tunai atau transfer manual langsung di tempat.
- **W-02 Pelacakan GPS Fisik Konsol:** Fitur pelacakan perangkat secara langsung (*real-time GPS tracking*) tidak dikerjakan karena konsol rental digunakan di dalam area tempat usaha (kecuali sewa khusus dengan jaminan identitas manual).

## 6. Matriks Keterlacakan (Traceability Matrix)

| User Story / Sumber | Kebutuhan Turunan (KF / KNF) | Keterangan / Status |
|---------------------|-------------------------------|---------------------|
| **US-01** (Pencatatan Transaksi Sewa Unit) | KF-01, KF-02, KF-03, KF-08 | Terkait langsung dengan siklus hidup transaksi sewa dan validasi data kasir. |
| **US-02** (Monitoring Ketersediaan Unit) | KF-04, KF-05, KNF-01 | Menjamin visibilitas real-time status konsol dan kecepatan akses dasbor. |
| **US-03** (Rekapitulasi Laporan Pendapatan) | KF-06, KF-07, KNF-03 | Menyediakan data laporan keuangan bagi pemilik dengan kontrol keamanan akses. |
| **Catatan Analisis / Mitigasi** | KNF-02, KNF-04, KF-09, KF-10 | Kebutuhan pendukung operasional, pencadangan data, kemudahan penggunaan, dan inventaris. |

## 7. Riwayat Konfirmasi Klien

| Tanggal Konfirmasi | Ringkasan Tanggapan / Masukan Klien | Perubahan yang Dilakukan pada SRS / PRD | Status Asumsi |
|--------------------|-------------------------------------|------------------------------------------|---------------|
| 11 November 2026   | Klien menyetujui seluruh fitur utama (pencatatan sewa, dasbor status, dan laporan omset). Klien meminta denda kelebihan waktu dihitung per 30 menit. Klien tidak memerlukan ekspor PDF untuk saat ini, cukup lihat di layar. | Memperbarui ketentuan denda pada PRD dan SRS; mengubah asumsi terkait ekspor laporan menjadi *Won't Have*. | Asumsi denda terjawab (menjadi pasti). |