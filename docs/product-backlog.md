# Product Backlog — Sistem Manajemen Rental PlayStation (Exito Playbox)

Dokumen ini memuat daftar produk backlog yang diturunkan langsung dari dokumen *Product Requirements Document* (PRD) dan Spesifikasi Kebutuhan Perangkat Lunak (SRS), terbagi ke dalam alokasi 4 sprint mingguan.

## Tabel Product Backlog dan Alokasi Sprint

| No | ID Kebutuhan | Butir Backlog (Fitur / Task) | Prioritas | Sprint Tentatif | Alasan / Catatan |
|----|--------------|------------------------------|-----------|-----------------|------------------|
| 1 | KF-01 | Implementasi tabel unit konsol dan fungsi ubah status unit (Tersedia / Terpakai) | Must | Sprint 1 | Fondasi utama operasional rental untuk melacak status fisik konsol. |
| 2 | KF-02 | Pembuatan logika kalkulasi durasi dan biaya sewa otomatis berbasis paket jam | Must | Sprint 1 | Fitur inti transaksi harian kasir untuk mencegah kesalahan hitung manual. |
| 3 | KF-04 | Pembuatan halaman dasbor monitoring status ketersediaan seluruh unit secara real-time | Must | Sprint 1 | Membantu operator melihat konsol yang kosong dengan cepat saat jam sibuk. |
| 4 | KF-03 | Penambahan modul penghentian timer dan kalkulasi denda/kelebihan waktu | Should | Sprint 2 | Menyempurnakan siklus transaksi saat waktu sewa habis atau melebihi paket. |
| 5 | KF-05 | Fitur penyaringan (*filtering*) daftar unit konsol berdasarkan jenis (PS3, PS4, PS5) | Could | Sprint 2 | Opsi tambahan untuk memudahkan pencarian unit spesifik. |
| 6 | KF-06 | Implementasi modul rekapitulasi laporan pendapatan harian dan bulanan | Must | Sprint 3 | Kebutuhan utama pemilik rental untuk memantau omset keuangan secara transparan. |
| 7 | KF-07 | Penyimpanan riwayat transaksi lengkap dengan data identitas penyewa ke database | Should | Sprint 3 | Memastikan data transaksi lampau dapat ditelusuri kembali untuk audit. |
| 8 | KF-08 | Validasi masukan (*input validation*) form transaksi kasir | Should | Sprint 3 | Mencegah masuknya data kosong atau tidak valid ke dalam sistem. |
| 9 | KF-09 & 10 | Pencatatan inventaris aksesori dan fitur pencarian riwayat transaksi lanjutan | Could | Sprint 4 | Fitur pelengkap opsional bila waktu pengembangan mencukupi. |

## Rincian Tugas Kecil Sprint 1 (Estimasi Durasi = 1 Hari Kerja per Tugas)
1. **[SK-01]** Membuat skema basis data SQLite dan tabel konsol, 	ransaksi, serta users (Estimasi: 0.5 hari).
2. **[SK-02]** Membangun kerangka dasar antarmuka web Flask menggunakan struktur folder 	emplates/ dan static/ (Estimasi: 0.5 hari).
3. **[SK-03]** Mengembangkan fungsi route Flask untuk menampilkan halaman dasbor utama (KF-04) (Estimasi: 1 hari).
4. **[SK-04]** Membuat form dan fungsi eksekusi untuk memulai sesi sewa serta mengubah status unit (KF-01) (Estimasi: 1 hari).
5. **[SK-05]** Menerapkan logika perhitungan biaya otomatis berdasarkan paket jam sewa (KF-02) (Estimasi: 1 hari).
