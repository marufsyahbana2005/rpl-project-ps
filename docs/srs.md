# Software Requirements Specification (SRS) - Sistem Rental PlayStation

## 1. Pendahuluan
Dokumen Spesifikasi Kebutuhan Perangkat Lunak ini mendeskripsikan fungsionalitas dan parameter kualitas sistem manajemen rental konsol Exito Playbox.

## 2. Deskripsi Umum
Sistem ini dirancang untuk mengelola data unit konsol, transaksi penyewaan berbasis waktu, manajemen anggota, serta rekapitulasi laporan pendapatan kasir dan pemilik.

## 3. Kebutuhan Fungsional

| ID | Pernyataan Kebutuhan | Sumber | Prioritas | Asumsi? | Hasil yang Diharapkan (Test Case) |
|----|----------------------|--------|-----------|---------|---------------------------------|
| KF-01 | Sistem harus mengubah status konsol menjadi terpakai saat transaksi sewa dimulai. | US-01 | Tinggi | Tidak | Status unit konsol berubah dari tersedia menjadi terpakai pada sistem. |
| KF-02 | Sistem harus menghitung durasi dan biaya sewa secara otomatis berdasarkan paket jam yang dipilih. | US-01 | Tinggi | Tidak | Total biaya sewa muncul akurat sesuai durasi penggunaan. |
| KF-03 | Sistem harus menghentikan timer aktif dan menghitung biaya denda atau kelebihan waktu secara otomatis. | US-01 | Tinggi | Tidak | Muncul rincian biaya tambahan saat waktu sewa melebihi batas paket. |
| KF-04 | Sistem harus menampilkan dasbor visual status ketersediaan seluruh unit konsol secara real-time. | US-02 | Tinggi | Tidak | Indikator warna unit (kosong/terpakai) langsung diperbarui di layar kasir. |
| KF-05 | Sistem harus menyaring daftar unit konsol berdasarkan jenis konsol (PS3, PS4, PS5). | US-02 | Sedang | Ya | Operator dapat memfilter unit konsol sesuai permintaan pelanggan. |
| KF-06 | Sistem harus merekapitulasi total pendapatan transaksi harian dan bulanan secara otomatis. | US-03 | Tinggi | Tidak | Laporan total omset harian tersaji tanpa perlu hitung manual. |
| KF-07 | Sistem harus menyimpan data riwayat transaksi sewa lengkap dengan identitas penyewa. | US-03 | Sedang | Ya | Data transaksi tersimpan di database dan dapat ditelusuri kembali. |
| KF-08 | Sistem harus memvalidasi input data kasir sebelum transaksi sewa baru disimpan ke database. | US-01 | Tinggi | Ya | Muncul peringatan jika ada kolom data wajib yang kosong. |
| KF-09 | Sistem harus mencatat pencatatan data inventaris aksesori pendukung seperti stik dan kabel. | Analisis | Sedang | Ya | Stok aksesori tambahan tercatat dan terpantau kondisinya. |
| KF-10 | Sistem harus menyediakan fitur pencarian data riwayat transaksi berdasarkan tanggal atau nama penyewa. | Analisis | Rendah | Ya | Data transaksi lama dapat ditemukan dengan cepat melalui kolom pencarian. |

## 4. Kebutuhan Non-Fungsional

| ID | Kategori | Pernyataan Terukur | Sumber |
|----|----------|--------------------|--------|
| KNF-01 | Kinerja | Halaman dasbor status unit harus terbuka dalam waktu kurang dari atau sama dengan 2 detik pada perangkat komputer kasir standar. | Catatan Wawancara No. 1 & Analisis |
| KNF-02 | Keandalan | Sistem harus melakukan pencadangan (*backup*) basis data otomatis minimal sekali setiap hari untuk mencegah kehilangan data transaksi saat terjadi kendala teknis. | Catatan Wawancara Analisis (Mitigasi Risiko) |
| KNF-03 | Keamanan | Akses ke menu rekapitulasi laporan keuangan dan pengaturan sistem dibatasi hanya untuk akun dengan peran pemilik (*owner*). | Catatan Wawancara No. 3 |
| KNF-04 | Kegunaan (*Usability*) | Antarmuka kasir harus dapat dioperasikan dengan mudah dan dipahami oleh pegawai baru dalam waktu pelatihan maksimal 15 menit tanpa panduan teknis yang rumit. | Catatan Wawancara Analisis (Karakteristik Pengguna) |
