# Spesifikasi Kebutuhan Perangkat Lunak (SRS) — Exito Playbox

Dokumen ini memuat spesifikasi kebutuhan perangkat lunak dan pemodelan sistem manajemen rental PlayStation Exito Playbox.

---

## 1. Pemodelan Sistem (UML)
Dokumen perancangan pemodelan sistem Exito Playbox tersimpan di dalam direktori `docs/uml/`:
- **Use Case Diagram:** [`docs/uml/use-case.mmd`](uml/use-case.mmd) | Visual: [`docs/uml/use-case.png`](uml/use-case.png)
- **Skenario Use Case:** [`docs/uml/skenario-use-case.md`](uml/skenario-use-case.md)
- **Activity Diagram Proses 1 (Catat Transaksi):** [`docs/uml/activity-01-catat-transaksi.mmd`](uml/activity-01-catat-transaksi.mmd)
- **Activity Diagram Proses 2 (Kelola Denda):** [`docs/uml/activity-02-kelola-denda.mmd`](uml/activity-02-kelola-denda.mmd)
- **Activity Diagram Proses 3 (Pantau Dasbor):** [`docs/uml/activity-03-pantau-dasbor.mmd`](uml/activity-03-pantau-dasbor.mmd)

---

## 2. Riwayat Konfirmasi Aturan Data (Data Rules Confirmation)

- **Tanggal Konfirmasi:** 16 November 2026
- **Metode:** Wawancara terstruktur & verifikasi batasan data kamus data
- **Narasumber (Klien):** Pemilik & Kepala Operasional Rental Exito Playbox
- **Pewawancara / Analis:** Maruf Syahbana (Product Owner & Developer)
- **Tujuan:** Mengonfirmasi batasan integritas data, aturan validasi bisnis, retensi data, dan penanganan kondisi tepi (*edge cases*) menggunakan bahasa awam yang dipahami pihak operasional.

### 2.1 Ringkasan Tanya-Jawab Aturan Data (Bahasa Awam)

| No | Topik / Entitas | Pertanyaan Konfirmasi (Bahasa Awam) | Jawaban & Arahan Klien | Implikasi Aturan Basis Data |
|:--:|---|---|---|---|
| **Q1** | **Data Pengguna (`users`)** | *"Kalau ada kasir yang sudah berhenti bekerja, apakah akunnya boleh dihapus dari aplikasi?"* | **Tidak boleh dihapus.** Kalau dihapus, laporan transaksi yang pernah dibuat kasir tersebut bisa hilang atau rancu. Cukup dinonaktifkan saja agar tidak bisa login lagi. | Tambahkan penanda status aktif (`is_active` bernilai `1` untuk aktif, `0` untuk nonaktif). Terapkan integritas `ON DELETE RESTRICT` pada relasi ke transaksi. |
| **Q2** | **Data Pengguna (`users`)** | *"Apakah boleh ada lebih dari satu akun Pemilik (Owner) di sistem?"* | **Cukup satu akun Owner.** Hanya pemilik utama yang berhak mengubah tarif paket, menambah konsol, dan melihat laporan keuangan penuh. | Batasan unik pada username dan penegakan logika bisnis satu akun owner aktif. |
| **Q3** | **Unit Konsol (`consoles`)** | *"Apakah jumlah konsol bisa minus? Kalau ada konsol yang rusak total, apakah datanya dihapus?"* | **Konsol adalah fisik nyata, tidak boleh minus.** Kalau rusak, jangan dihapus dari daftar karena ada riwayat sewanya; ubah saja statusnya jadi *'maintenance'* (perbaikan/rusak). | Stok/unit terdaftar sebagai entitas unik (`kode_konsol UNIQUE`). Unit rusak tidak di-hard delete, melainkan status `'maintenance'`. Relasi `ON DELETE RESTRICT`. |
| **Q4** | **Unit Konsol (`consoles`)** | *"Apakah ada jenis konsol selain PS3, PS4, dan PS5 yang disewakan sekarang atau dalam waktu dekat?"* | **Saat ini hanya 3 jenis itu.** Belum ada rencana menambah Nintendo Switch atau konsol lain. | Batasan `CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5'))` dipertahankan dan divalidasi ketat. |
| **Q5** | **Unit Konsol (`consoles`)** | *"Apakah satu konsol yang sedang main boleh dipakai oleh pelanggan lain di jam yang sama?"* | **Tidak boleh sama sekali.** Satu unit hanya bisa aktif untuk satu sesi sewa sampai sesi tersebut dihentikan/selesai. | Validasi sistem: Konsol yang berstatus `'terpakai'` tidak dapat dipilih untuk transaksi baru sampai status kembali `'tersedia'`. |
| **Q6** | **Paket Sewa (`packages`)** | *"Apakah harga paket sewa boleh berbeda antar-pelanggan (misal ada tawar-menawar)?"* | **Tidak boleh berbeda antarpelanggan.** Harga sewa wajib seragam dan transparan mengikuti paket resmi agar kasir tidak memanipulasi tarif. | Tarif sewa dikunci pada tabel master `packages` (`harga >= 0`), kasir memilih paket baku tanpa input bebas nilai rupiah sewa. |
| **Q7** | **Paket Sewa (`packages`)** | *"Apakah tarif sewa PS3, PS4, dan PS5 sama, atau berbeda?"* | **Berbeda.** Main PS3 paling murah (misal Rp 8.000/jam), PS4 (Rp 12.000/jam), dan PS5 (Rp 20.000/jam). Jadi tiap paket harus jelas untuk jenis konsol apa. | Tambahkan atribut `jenis_konsol` pada tabel `packages` (`CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5'))`) agar paket terikat pada tipe konsol terkait. |
| **Q8** | **Paket Sewa (`packages`)** | *"Apakah boleh ada harga paket Rp 0 (gratis)?"* | **Boleh.** Terkadang kami adakan promo bonus main 1 jam gratis untuk langganan atau pemenang turnamen rental. | Batasan `CHECK (harga >= 0)` dipertahankan (bukan `harga > 0`). |
| **Q9** | **Paket Sewa (`packages`)** | *"Jika paket promo lama sudah selesai/kedaluwarsa, apakah boleh dihapus?"* | **Jangan dihapus.** Kalau dihapus, data nota lama yang pakai paket itu jadi rusak. Cukup disembunyikan/dinonaktifkan agar kasir tidak bisa memilihnya lagi. | Tambahkan kolom status aktif paket (`is_active INTEGER NOT NULL DEFAULT 1`). Transaksi lama tetap mengacu pada `package_id` tanpa error foreign key. |
| **Q10** | **Identitas Pelanggan (`transactions`)** | *"Apakah kasir perlu mencatat nama pelanggan saat mulai sewa, atau sistem rental anonim?"* | **Wajib catat nama panggilan/pelanggan.** Saat rental ramai dengan 8 unit menyala bersamaan, kasir sering lupa siapa yang sedang main di TV tertentu. | Tambahkan kolom `nama_pelanggan TEXT NOT NULL` pada tabel `transactions`. |
| **Q11** | **Pembatalan Transaksi (`transactions`)** | *"Bagaimana jika pelanggan baru main 2 menit tiba-tiba mati lampu atau ada kendala mendesak sehingga harus batal main?"* | **Boleh dibatalkan.** Asalkan pembatalan dilakukan kasir maksimal 5 menit pertama, transaksi dianggap batal dan tidak dihitung ke omset harian. | Tambahkan status pembayaran/transaksi `'batal'`: `CHECK (status_bayar IN ('lunas', 'open_bill', 'batal'))`. |
| **Q12** | **Retensi Data (`transactions`)** | *"Apakah riwayat transaksi lama boleh dihapus setelah beberapa bulan? Berapa lama data harus disimpan?"* | **Tidak boleh dihapus sama sekali (disimpan permanen, minimal 3-5 tahun).** Data ini dibutuhkan untuk audit pendapatan tahunan, evaluasi unit paling laris, dan rekap keuangan pemilik. | Terapkan kebijakan *No Hard Delete* untuk data transaksional. Semua relasi ke master menggunakan `ON DELETE RESTRICT`. |
| **Q13** | **Denda & Toleransi (`fines`)** | *"Apakah keterlambatan 1 atau 2 menit langsung kena denda uang?"* | **Tidak langsung denda. Ada toleransi (grace period) 5 menit.** Pelanggan butuh waktu menyimpan game (*save game*) dan mengembalikan stik. Lewat dari 5 menit baru kena denda kelipatan per 15 menit. | Logika hitung denda: jika `menit_terlambat <= 5`, maka `biaya_denda = 0`. Jika `> 5`, dihitung proporsional pembulatan 15 menit. |
| **Q14** | **Denda Toleransi Khusus (`fines`)** | *"Apakah denda boleh diikhlaskan/dibebaskan (Rp 0) oleh kasir atau pemilik?"* | **Boleh Rp 0.** Jika ada kompensasi kendala stik/game macet, denda dapat dihapuskan/dinolkan, namun durasi keterlambatan tetap tercatat untuk arsip. | Batasan `biaya_denda >= 0` dan `menit_terlambat >= 0` dipertahankan. |

---

### 2.2 Keputusan Desain & Tindak Lanjut Perubahan
Berdasarkan hasil konfirmasi aturan data dengan klien, disepakati butir penyesuaian desain basis data:
1. **Tabel `users`:** Menambahkan kolom `is_active` (`INTEGER`, default `1`) untuk mendukung penonaktifan akun staf tanpa menghapus integritas audit.
2. **Tabel `packages`:** Menambahkan kolom `jenis_konsol` (`TEXT`, wajib) agar tarif paket spesifik terhadap tipe konsol (PS3/PS4/PS5), serta menambahkan kolom `is_active` (`INTEGER`, default `1`) untuk *soft-delete* paket promo.
3. **Tabel `transactions`:** Menambahkan kolom `nama_pelanggan` (`TEXT`, wajib diisi oleh kasir saat membuka rental), serta memperluas nilai constraint `status_bayar` dengan menambahkan opsi status `'batal'`.
4. **Tabel `consoles` & `fines`:** Mempertahankan seluruh constraint integritas referensial dan batas non-negatif yang sudah ada, serta menegaskan aturan bisnis *grace period* 5 menit pada tingkat logika aplikasi.


---

## 2. Riwayat Konfirmasi Aturan Data (Data Rules Confirmation)

- **Tanggal Konfirmasi:** 16 November 2026
- **Metode:** Wawancara terstruktur & verifikasi batasan data kamus data
- **Narasumber (Klien):** Pemilik & Kepala Operasional Rental Exito Playbox
- **Pewawancara / Analis:** Maruf Syahbana (Product Owner & Developer)
- **Tujuan:** Mengonfirmasi batasan integritas data, aturan validasi bisnis, retensi data, dan penanganan kondisi tepi (*edge cases*) menggunakan bahasa awam yang dipahami pihak operasional.

### 2.1 Ringkasan Tanya-Jawab Aturan Data (Bahasa Awam)

| No | Topik / Entitas | Pertanyaan Konfirmasi (Bahasa Awam) | Jawaban & Arahan Klien | Implikasi Aturan Basis Data |
|:--:|---|---|---|---|
| **Q1** | **Data Pengguna (`users`)** | *"Kalau ada kasir yang sudah berhenti bekerja, apakah akunnya boleh dihapus dari aplikasi?"* | **Tidak boleh dihapus.** Kalau dihapus, laporan transaksi yang pernah dibuat kasir tersebut bisa hilang atau rancu. Cukup dinonaktifkan saja agar tidak bisa login lagi. | Tambahkan penanda status aktif (`is_active` bernilai `1` untuk aktif, `0` untuk nonaktif). Terapkan integritas `ON DELETE RESTRICT` pada relasi ke transaksi. |
| **Q2** | **Data Pengguna (`users`)** | *"Apakah boleh ada lebih dari satu akun Pemilik (Owner) di sistem?"* | **Cukup satu akun Owner.** Hanya pemilik utama yang berhak mengubah tarif paket, menambah konsol, dan melihat laporan keuangan penuh. | Batasan unik pada username dan penegakan logika bisnis satu akun owner aktif. |
| **Q3** | **Unit Konsol (`consoles`)** | *"Apakah jumlah konsol bisa minus? Kalau ada konsol yang rusak total, apakah datanya dihapus?"* | **Konsol adalah fisik nyata, tidak boleh minus.** Kalau rusak, jangan dihapus dari daftar karena ada riwayat sewanya; ubah saja statusnya jadi *'maintenance'* (perbaikan/rusak). | Stok/unit terdaftar sebagai entitas unik (`kode_konsol UNIQUE`). Unit rusak tidak di-hard delete, melainkan status `'maintenance'`. Relasi `ON DELETE RESTRICT`. |
| **Q4** | **Unit Konsol (`consoles`)** | *"Apakah ada jenis konsol selain PS3, PS4, dan PS5 yang disewakan sekarang atau dalam waktu dekat?"* | **Saat ini hanya 3 jenis itu.** Belum ada rencana menambah Nintendo Switch atau konsol lain. | Batasan `CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5'))` dipertahankan dan divalidasi ketat. |
| **Q5** | **Unit Konsol (`consoles`)** | *"Apakah satu konsol yang sedang main boleh dipakai oleh pelanggan lain di jam yang sama?"* | **Tidak boleh sama sekali.** Satu unit hanya bisa aktif untuk satu sesi sewa sampai sesi tersebut dihentikan/selesai. | Validasi sistem: Konsol yang berstatus `'terpakai'` tidak dapat dipilih untuk transaksi baru sampai status kembali `'tersedia'`. |
| **Q6** | **Paket Sewa (`packages`)** | *"Apakah harga paket sewa boleh berbeda antar-pelanggan (misal ada tawar-menawar)?"* | **Tidak boleh berbeda antarpelanggan.** Harga sewa wajib seragam dan transparan mengikuti paket resmi agar kasir tidak memanipulasi tarif. | Tarif sewa dikunci pada tabel master `packages` (`harga >= 0`), kasir memilih paket baku tanpa input bebas nilai rupiah sewa. |
| **Q7** | **Paket Sewa (`packages`)** | *"Apakah tarif sewa PS3, PS4, dan PS5 sama, atau berbeda?"* | **Berbeda.** Main PS3 paling murah (misal Rp 8.000/jam), PS4 (Rp 12.000/jam), dan PS5 (Rp 20.000/jam). Jadi tiap paket harus jelas untuk jenis konsol apa. | Tambahkan atribut `jenis_konsol` pada tabel `packages` (`CHECK (jenis_konsol IN ('PS3', 'PS4', 'PS5'))`) agar paket terikat pada tipe konsol terkait. |
| **Q8** | **Paket Sewa (`packages`)** | *"Apakah boleh ada harga paket Rp 0 (gratis)?"* | **Boleh.** Terkadang kami adakan promo bonus main 1 jam gratis untuk langganan atau pemenang turnamen rental. | Batasan `CHECK (harga >= 0)` dipertahankan (bukan `harga > 0`). |
| **Q9** | **Paket Sewa (`packages`)** | *"Jika paket promo lama sudah selesai/kedaluwarsa, apakah boleh dihapus?"* | **Jangan dihapus.** Kalau dihapus, data nota lama yang pakai paket itu jadi rusak. Cukup disembunyikan/dinonaktifkan agar kasir tidak bisa memilihnya lagi. | Tambahkan kolom status aktif paket (`is_active INTEGER NOT NULL DEFAULT 1`). Transaksi lama tetap mengacu pada `package_id` tanpa error foreign key. |
| **Q10** | **Identitas Pelanggan (`transactions`)** | *"Apakah kasir perlu mencatat nama pelanggan saat mulai sewa, atau sistem rental anonim?"* | **Wajib catat nama panggilan/pelanggan.** Saat rental ramai dengan 8 unit menyala bersamaan, kasir sering lupa siapa yang sedang main di TV tertentu. | Tambahkan kolom `nama_pelanggan TEXT NOT NULL` pada tabel `transactions`. |
| **Q11** | **Pembatalan Transaksi (`transactions`)** | *"Bagaimana jika pelanggan baru main 2 menit tiba-tiba mati lampu atau ada kendala mendesak sehingga harus batal main?"* | **Boleh dibatalkan.** Asalkan pembatalan dilakukan kasir maksimal 5 menit pertama, transaksi dianggap batal dan tidak dihitung ke omset harian. | Tambahkan status pembayaran/transaksi `'batal'`: `CHECK (status_bayar IN ('lunas', 'open_bill', 'batal'))`. |
| **Q12** | **Retensi Data (`transactions`)** | *"Apakah riwayat transaksi lama boleh dihapus setelah beberapa bulan? Berapa lama data harus disimpan?"* | **Tidak boleh dihapus sama sekali (disimpan permanen, minimal 3-5 tahun).** Data ini dibutuhkan untuk audit pendapatan tahunan, evaluasi unit paling laris, dan rekap keuangan pemilik. | Terapkan kebijakan *No Hard Delete* untuk data transaksional. Semua relasi ke master menggunakan `ON DELETE RESTRICT`. |
| **Q13** | **Denda & Toleransi (`fines`)** | *"Apakah keterlambatan 1 atau 2 menit langsung kena denda uang?"* | **Tidak langsung denda. Ada toleransi (grace period) 5 menit.** Pelanggan butuh waktu menyimpan game (*save game*) dan mengembalikan stik. Lewat dari 5 menit baru kena denda kelipatan per 15 menit. | Logika hitung denda: jika `menit_terlambat <= 5`, maka `biaya_denda = 0`. Jika `> 5`, dihitung proporsional pembulatan 15 menit. |
| **Q14** | **Denda Toleransi Khusus (`fines`)** | *"Apakah denda boleh diikhlaskan/dibebaskan (Rp 0) oleh kasir atau pemilik?"* | **Boleh Rp 0.** Jika ada kompensasi kendala stik/game macet, denda dapat dihapuskan/dinolkan, namun durasi keterlambatan tetap tercatat untuk arsip. | Batasan `biaya_denda >= 0` dan `menit_terlambat >= 0` dipertahankan. |

---

### 2.2 Keputusan Desain & Tindak Lanjut Perubahan
Berdasarkan hasil konfirmasi aturan data dengan klien, disepakati butir penyesuaian desain basis data:
1. **Tabel `users`:** Menambahkan kolom `is_active` (`INTEGER`, default `1`) untuk mendukung penonaktifan akun staf tanpa menghapus integritas audit.
2. **Tabel `packages`:** Menambahkan kolom `jenis_konsol` (`TEXT`, wajib) agar tarif paket spesifik terhadap tipe konsol (PS3/PS4/PS5), serta menambahkan kolom `is_active` (`INTEGER`, default `1`) untuk *soft-delete* paket promo.
3. **Tabel `transactions`:** Menambahkan kolom `nama_pelanggan` (`TEXT`, wajib diisi oleh kasir saat membuka rental), serta memperluas nilai constraint `status_bayar` dengan menambahkan opsi status `'batal'`.
4. **Tabel `consoles` & `fines`:** Mempertahankan seluruh constraint integritas referensial dan batas non-negatif yang sudah ada, serta menegaskan aturan bisnis *grace period* 5 menit pada tingkat logika aplikasi.