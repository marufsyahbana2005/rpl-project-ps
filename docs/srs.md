# Spesifikasi Kebutuhan Perangkat Lunak (SRS) — Exito Playbox

## 1. Pendahuluan
Dokumen Spesifikasi Kebutuhan Perangkat Lunak ini mendeskripsikan fungsionalitas, parameter kualitas, batasan prioritas, pemodelan UML, riwayat konfirmasi aturan data, serta matriks keterlacakan sistem manajemen rental konsol Exito Playbox.

## 2. Deskripsi Umum
Sistem ini dirancang untuk mengelola data unit konsol, transaksi penyewaan berbasis waktu (*timer billing*), pencegahan galat input kasir, penanganan denda keterlambatan secara adil, serta rekapitulasi laporan pendapatan pemilik rental (*owner*).

## 3. Kebutuhan Fungsional

| ID | Pernyataan Kebutuhan | Sumber | Prioritas | Asumsi? | Kolom Uji / Test Case Verifikasi |
|:--:|---|:--:|:--:|:--:|:--:|
| **KF-01** | Sistem harus mengubah status konsol menjadi terpakai saat transaksi sewa dimulai. | US-01 | **Must** | Tidak | **TC-01, TC-02** |
| **KF-02** | Sistem harus menghitung durasi dan biaya sewa secara otomatis berdasarkan paket jam yang dipilih. | US-01 | **Must** | Tidak | **TC-03, TC-04** |
| **KF-03** | Sistem harus menghentikan timer aktif dan menghitung biaya denda atau kelebihan waktu secara otomatis. | US-01 | **Should** | Tidak | **TC-05, TC-06** |
| **KF-04** | Sistem harus menampilkan dasbor visual status ketersediaan seluruh unit konsol secara real-time. | US-02 | **Must** | Tidak | **TC-07** |
| **KF-05** | Sistem harus menyaring daftar unit konsol berdasarkan jenis konsol (PS3, PS4, PS5). | US-02 | Could | Ya | TC-Filt-01 |
| **KF-06** | Sistem harus merekapitulasi total pendapatan transaksi harian dan bulanan secara otomatis. | US-03 | **Must** | Tidak | **TC-08** |
| **KF-07** | Sistem harus menyimpan data riwayat transaksi sewa lengkap dengan identitas penyewa. | US-03 | **Should** | Ya | **TC-10** |
| **KF-08** | Sistem harus memvalidasi input data kasir sebelum transaksi sewa baru disimpan ke database. | US-01 | **Should** | Ya | **TC-09** |
| **KF-09** | Sistem harus mencatat pencatatan data inventaris aksesori pendukung seperti stik dan kabel. | Analisis | Could | Ya | TC-Inv-01 |
| **KF-10** | Sistem harus menyediakan fitur pencarian data riwayat transaksi berdasarkan tanggal atau nama penyewa. | Analisis | Rendah | Ya | **TC-10** |

## 4. Kebutuhan Non-Fungsional

| ID | Kategori | Pernyataan Terukur | Sumber | Prioritas | Kolom Uji / Test Case |
|:--:|---|---|:--:|:--:|:--:|
| **KNF-01** | Kinerja | Halaman dasbor status unit harus terbuka dalam waktu $\le 2$ detik pada perangkat komputer kasir standar. | Catatan Wawancara No. 1 | **Must** | **TC-07** |
| **KNF-02** | Keandalan | Sistem harus melakukan pencadangan (*backup*) basis data otomatis minimal sekali setiap hari untuk mencegah kehilangan data transaksi. | Catatan Wawancara Analisis | **Should** | TC-Back-01 |
| **KNF-03** | Keamanan | Akses ke menu rekapitulasi laporan keuangan dan pengaturan sistem dibatasi hanya untuk akun dengan peran pemilik (*owner*). | Catatan Wawancara No. 3 | **Must** | **TC-11** |
| **KNF-04** | Kegunaan (*Usability*) | Antarmuka kasir harus dapat dioperasikan dengan mudah dan dipahami oleh pegawai baru dalam waktu pelatihan maksimal 15 menit. | Catatan Wawancara Analisis | **Should** | UAT-Usab-01 |

## 5. Batasan dan Fitur yang Tidak Dikerjakan (Won't Have)
- **W-01 Integrasi Payment Gateway Otomatis:** Pembayaran digital otomatis melalui API pihak ketiga ditiadakan; pembayaran dilakukan secara tunai atau transfer manual di tempat.
- **W-02 Pelacakan GPS Fisik Konsol:** Fitur pelacakan perangkat secara langsung tidak disertakan karena unit dioperasikan di dalam area rental.
- **W-03 Ekspor Dokumen Laporan PDF/Excel:** Berdasarkan konfirmasi klien, laporan disajikan langsung di layar aplikasi tanpa ekspor berkas eksternal.

---

## 6. Pemodelan Sistem (UML)
Dokumen perancangan pemodelan sistem Exito Playbox tersimpan di dalam direktori `docs/uml/`:
- **Use Case Diagram:** [`docs/uml/use-case.mmd`](uml/use-case.mmd)
- **Skenario Use Case:** [`docs/uml/skenario-use-case.md`](uml/skenario-use-case.md)
- **Activity Diagram Proses 1 (Catat Transaksi):** [`docs/uml/activity-01-catat-transaksi.mmd`](uml/activity-01-catat-transaksi.mmd)
- **Activity Diagram Proses 2 (Kelola Denda):** [`docs/uml/activity-02-kelola-denda.mmd`](uml/activity-02-kelola-denda.mmd)
- **Activity Diagram Proses 3 (Pantau Dasbor):** [`docs/uml/activity-03-pantau-dasbor.mmd`](uml/activity-03-pantau-dasbor.mmd)

---

## 7. Riwayat Konfirmasi Aturan Data (Data Rules Confirmation)

- **Tanggal Konfirmasi:** 16 November 2026
- **Metode:** Wawancara terstruktur & verifikasi batasan data kamus data
- **Narasumber (Klien):** Pemilik & Kepala Operasional Rental Exito Playbox
- **Pewawancara / Analis:** Maruf Syahbana (Product Owner & Developer)
- **Tujuan:** Mengonfirmasi batasan integritas data, aturan validasi bisnis, retensi data, dan penanganan kondisi tepi (*edge cases*) menggunakan bahasa awam yang dipahami pihak operasional.

### 7.1 Ringkasan Tanya-Jawab Aturan Data (Bahasa Awam)

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

## 8. Matriks Keterlacakan (Traceability Matrix) — Diperbarui dengan Test Case (Langkah 9)

| User Story / Sumber | Kebutuhan Turunan (KF / KNF) | Use Case Terkait | Halaman Antarmuka | Prioritas | Kolom Uji (Test Case) |
|---|---|:--:|---|:--:|:--:|
| **US-01** (Pencatatan Transaksi Sewa Unit) | **KF-01** (Status Konsol) | UC-01 | `wf-02` Dasbor Utama<br>`wf-03` Buka Sewa | **Must** | **TC-01, TC-02** |
| **US-01** (Kalkulasi Otomatis Durasi & Tarif) | **KF-02** (Biaya Paket Sewa) | UC-01 | `wf-03` Buka Sewa | **Must** | **TC-03, TC-04** |
| **US-01** (Penanganan Keterlambatan Sewa) | **KF-03** (Kalkulasi Denda) | UC-02 | `wf-04` Selesai Sewa & Denda | **Should** | **TC-05, TC-06** |
| **US-01** (Pencegahan Kesalahan Kasir) | **KF-08** (Validasi Input) | UC-01 | `wf-03` Buka Sewa | **Should** | **TC-09** |
| **US-02** (Monitoring Ketersediaan Unit) | **KF-04** (Dasbor Real-time) | UC-03 | `wf-02` Dasbor Utama | **Must** | **TC-07** |
| **US-02** (Kinerja Pemuatan Antarmuka) | **KNF-01** (Respon $\le 2$ Detik) | UC-03 | `wf-02` Dasbor Utama | **Must** | **TC-07** |
| **US-03** (Rekapitulasi Omset Finansial) | **KF-06** (Laporan Omset) | UC-04 | `wf-07` Laporan Pendapatan | **Must** | **TC-08** |
| **US-03** (Penelusuran Audit Transaksi) | **KF-07** (Riwayat Transaksi) | UC-05 | `wf-06` Riwayat Transaksi | **Should** | **TC-10** |
| **US-03** (Keamanan Data Finansial) | **KNF-03** (Otorisasi Role Owner) | UC-04 | `wf-05` Kelola Master<br>`wf-07` Laporan Pendapatan | **Must** | **TC-11** |
