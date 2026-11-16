# Lembar Tinjauan Rancangan Antarmuka & Rencana Uji (Design Review) — Langkah 11

- **Kelompok yang Ditinjau:** Kelompok Exito Playbox (Maruf Syahbana)
- **Kelompok Penelaah:** Kelompok Mitra / Penelaah Antarkelompok (Rental Management Peer Reviewer)
- **Tanggal Sesi:** 16 November 2026

---

## 1. Kekuatan Rancangan (Minimal 1 Kekuatan)
1. **Kejelasan Peta Navigasi dan Hirarki Klik:**  
   Peta navigasi yang dirancang sangat jelas dan efisien. Seluruh 7 halaman dapat dicapai dalam 1 hingga 2 kali klik dari Dasbor Utama. Pemisahan hak akses antara kasir dan pemilik (role-based restriction) terlihat jelas dengan penandaan visual warna kuning pada simpul khusus pemilik.
2. **Detail Komprehensif Antarmuka dan Penanganan Kasus Tepi:**  
   Wireframe `wf-04` (Selesai Sewa) dan `wf-03` (Buka Sewa) secara nyata menggambarkan kondisi galat dan aturan bisnis spesifik rental, seperti toleransi keterlambatan 5 menit (*grace period*), tombol pembatalan sewa darurat saat mati lampu, serta alert validasi input nama pelanggan.
3. **Keterlacakan Test Case yang Sangat Ketat:**  
   Daftar test case pada dokumen `rencana-uji.md` memiliki nilai batas terukur (misal TC-05 keterlambatan tepat 5 menit vs TC-06 keterlambatan 6 menit) yang langsung merujuk pada kebutuhan PRD dan kamus data.

---

## 2. Saran dan Temuan Beralasan (Minimal 2 Saran/Temuan)
1. **Temuan / Saran 1 — Tombol Konfirmasi Pembatalan Sewa:**  
   *Temuan:* Pada wireframe `wf-04`, tombol `[X] Batalkan Sewa (Mati Lampu)` berada persis di sebelah tombol `Konfirmasi Bayar`. Jika kasir salah klik secara tidak sengaja (*accidental click*), transaksi sewa bisa langsung terhapus/dibatalkan tanpa sengaja.  
   *Saran:* Berikan dialog konfirmasi (*modal confirmation popup*) bertuliskan *"Apakah Anda yakin ingin membatalkan transaksi ini karena kendala teknis?"* sebelum status `'batal'` diterapkan.
2. **Temuan / Saran 2 — Indikator Suara atau Pop-up Waktu Habis pada Dasbor:**  
   *Temuan:* Pada dasbor utama `wf-02`, status unit yang habis waktu hanya ditandai dengan perubahan status teks kuning `OVERTIME`. Saat jam ramai dan kasir sedang melayani pelanggan lain di meja nota, perubahan warna visual saja mungkin terlewat dari pandangan kasir.  
   *Saran:* Tambahkan indikator visual yang berkedip atau bunyi notifikasi alarm singkat (*audio alert*) ketika timer unit menyentuh angka 00:00:00 agar kasir segera mendatangi pelanggan.
3. **Temuan / Saran 3 — Cetak Struk / Nota Fisik Mini:**  
   *Temuan:* Pada `wf-04`, setelah kasir mengklik konfirmasi bayar, data transaksi langsung masuk ke database, namun belum ada opsi cetak struk thermal mini 58mm untuk pelanggan yang membutuhkan bukti pembayaran kertas.  
   *Saran:* Pertimbangkan penambahan tombol opsional `[Cetak Struk]` pada halaman konfirmasi pembayaran atau detail riwayat transaksi.

---

## 3. Pertanyaan Kritis untuk Kelompok yang Ditinjau (Minimal 1 Pertanyaan)
1. **Pertanyaan 1:**  
   *"Bagaimana sistem menangani situasi di mana koneksi jaringan internet atau WiFi lokal terputus saat kasir sedang memproses transaksi di halaman `wf-03` atau `wf-04`? Apakah data timer sewa tetap akurat di sisi server?"*
2. **Pertanyaan 2:**  
   *"Apakah pemilik dapat melihat rincian unit konsol mana yang paling sering rusak atau paling sering masuk status Maintenance pada laporan bulanan?"*
