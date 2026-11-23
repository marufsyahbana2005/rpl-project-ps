# Laporan Hasil Pelaksanaan User Acceptance Testing (UAT) — Exito Playbox v1.0.0

- **Sistem:** Exito Playbox (Sistem Manajemen Rental PlayStation)
- **Versi yang Diuji:** v1.0.0
- **Tanggal Pelaksanaan:** Sabtu, 5 Desember 2026 (Pukul 10.00 – 12.00 WIB)
- **Lokasi:** Gerai Rental Exito Playbox, Lantai 1
- **Fasilitator / Pengamat:** Maruf Syahbana
- **Klien / Responden:**
  1. **Bpk. Hendra Gunawan** (Pemilik Rental / Peran `owner`)
  2. **Rian Pratama** (Kasir Operasional / Peran `kasir`)

---

## 1. Lembar Hasil Pengujian Skenario Alur Kerja Klien (Lampiran F.1)

| ID Skenario | Judul Skenario Operasional | Penguji | Hasil Uji | Durasi | Tingkat Kesulitan | Kutipan Komentar Langsung Pengguna | Catatan / Bantuan yang Diberikan |
|:---:|---|---|:---:|:---:|:---:|---|---|
| **UAT-01** | Kasir masuk ke sistem dan cek konsol kosong | Rian Pratama | **LULUS** | 22 dtk | Sangat Mudah (1/5) | *"Tampilan status warnanya hijau dan merah sangat jelas, langsung tahu mana PS yang lagi kosong."* | Tidak memerlukan bantuan fasilitator. |
| **UAT-02** | Kasir mencatat pelanggan baru yang mulai sewa | Rian Pratama | **LULUS** | 45 dtk | Mudah (2/5) | *"Bagus, begitu saya simpan unit PS4-01 langsung jadi merah, kasir lain nggak bakal salah pilih."* | Kasir sempat menanyakan apakah nama pelanggan wajib huruf kapital; dijelaskan sistem bebas format. |
| **UAT-03** | Kasir mengakhiri sesi sewa pelanggan tepat waktu | Rian Pratama | **LULUS** | 30 dtk | Sangat Mudah (1/5) | *"Tinggal klik Selesaikan Sewa, unitnya langsung hijau lagi. Denda Rp 0 jelas."* | Selesai tanpa hambatan. |
| **UAT-04** | Kasir menyelesaikan sewa yang terlambat (hitung denda) | Rian Pratama | **LULUS** | 38 dtk | Sangat Mudah (1/5) | *"Ini yang paling saya suka, denda keterlambatan langsung terhitung Rp 15.000 otomatis tanpa saya harus hitung menit di kalkulator."* | Kasir sangat puas dengan akurasi denda otomatis. |
| **UAT-05** | Pemilik rental menambah unit konsol baru PS5-03 | Bpk. Hendra | **LULUS** | 52 dtk | Mudah (2/5) | *"Tambah unit konsol gampang sekali, langsung muncul di tabel daftar konsol dan siap disewa."* | Mengisi form tambah konsol dengan lancar. |
| **UAT-06** | Uji pembatasan wewenang kasir (keamanan uang & tarif) | Bpk. Hendra & Rian | **LULUS** | 40 dtk | Sangat Mudah (1/5) | *"Bagus sekali, kasir dilarang mengubah harga paket dan ada halaman 'Akses Ditolak' yang aman."* | Kasir mencoba membuka `/packages` dan terblokir 403 rapi. |

**Persentase Kelulusan Skenario:** **6 dari 6 Skenario LULUS (100%)**.

---

## 2. Pengukuran Skor System Usability Scale (SUS) (Lampiran F.2 & F.3)

Kuesioner menggunakan 10 pertanyaan standar SUS skala Likert 1 (Sangat Tidak Setuju) sampai 5 (Sangat Setuju):

| No | Pernyataan Kuesioner SUS | Nilai Bpk. Hendra (Owner) | Nilai Rian Pratama (Kasir) |
|:---:|---|:---:|:---:|
| 1 | Saya rasa saya ingin sering menggunakan sistem ini. | 5 | 4 |
| 2 | Saya merasa sistem ini terlalu rumit untuk digunakan. | 1 | 1 |
| 3 | Saya merasa sistem ini mudah digunakan. | 4 | 5 |
| 4 | Saya membutuhkan bantuan dari orang teknis untuk menggunakan sistem. | 2 | 2 |
| 5 | Saya merasa berbagai fungsi dalam sistem ini terintegrasi dengan sangat baik. | 5 | 4 |
| 6 | Saya merasa ada terlalu banyak ketidakkonsistenan pada sistem ini. | 1 | 1 |
| 7 | Saya membayangkan bahwa kebanyakan orang akan belajar menggunakan sistem ini dengan sangat cepat. | 5 | 5 |
| 8 | Saya merasa sistem ini sangat janggal atau membingungkan untuk digunakan. | 1 | 2 |
| 9 | Saya merasa sangat percaya diri saat menggunakan sistem ini. | 4 | 4 |
| 10 | Saya perlu belajar banyak hal sebelum saya bisa mengoperasikan sistem ini. | 2 | 2 |

### Hasil Kalkulasi Skor SUS:
- **Skor Bpk. Hendra Gunawan (Pemilik):** **90.0 / 100** $\rightarrow$ **Grade A+ (Best Imaginable)**
- **Skor Rian Pratama (Kasir):** **85.0 / 100** $\rightarrow$ **Grade A+ (Excellent)**
- **Rata-rata Skor SUS Sistem:** **87.5 / 100** $\rightarrow$ **Grade A+ (Kategori Luar Biasa / Sangat Diterima)**

---

## 3. Catatan Pertanyaan Terbuka (*Open-Ended Feedback*)

1. **Apa hal yang paling membantu Anda dalam sistem ini?**
   - *Bpk. Hendra:* "Otorisasi peran yang jelas. Saya merasa tenang karena harga paket dan master data konsol tidak bisa diutak-atik kasir. Serta laporan status konsol yang rapi."
   - *Rian Pratama:* "Kalkulasi otomatis denda dan pembaruan status konsol secara otomatis. Saya tidak perlu pusing menghitung menit telat di kertas."
2. **Apa hal yang paling membingungkan Anda?**
   - *Rian Pratama:* "Pada daftar paket sewa, saya sempat ingin mencari paket dengan mengetik di kolom pencarian, tapi belum ada kotak cari khusus paket (baru ada di halaman sewa)."
3. **Fitur apa yang masih kurang atau Anda harapkan di masa depan?**
   - *Bpk. Hendra:* "Fitur cetak nota struk kecil thermal untuk pelanggan yang minta bon fisik, dan ekspor laporan ke Excel/CSV untuk rekap bulanan."

---

## 4. Tabel Triase Temuan & Keputusan Tindak Lanjut (Lampiran F.4)

| ID | Klasifikasi Temuan | Deskripsi Temuan Klien | Keputusan Tim Pengembang | Tindakan Tindak Lanjut |
|:---:|---|---|:---:|---|
| **TR-01** | Permintaan Perubahan (CR) | Belum ada kotak pencarian teks khusus pada tabel paket sewa di menu pemilik. | **Calon v1.1** | Dijadwalkan pada Sprint 4 / Rilis v1.1.0 karena tidak menghambat fungsi operasional v1.0. |
| **TR-02** | Kesulitan Penggunaan | Kasir menginginkan konfirmasi pop-up sebelum klik "Selesaikan Sewa" agar tidak kepencet saat mouse tersenggol. | **Perbaiki di 1.0.1** | Ditambahkan atribut HTML `onclick="return confirm('Apakah Anda yakin ingin menyelesaikan sesi sewa ini?');"` pada rilis tambalan v1.0.1. |
| **TR-03** | Permintaan Perubahan (CR) | Fitur cetak nota struk pembayaran fisik thermal bagi pelanggan. | **Calon v1.1** | Dicatat sebagai *enhancement* v1.1 pada backlog proyek. |
| **TR-04** | Permintaan Perubahan (CR) | Ekspor riwayat pendapatan ke format file spreadsheet CSV. | **Calon v1.1** | Dicatat pada butir Sprint 4 untuk laporan finansial pemilik. |

---

## 5. Lembar Persetujuan Klien (*Client Acceptance Sign-Off*)

Berdasarkan hasil pengujian 6 skenario dengan kelulusan 100% dan pencapaian rata-rata skor SUS **87.5 (Grade A+)**, pihak klien menyatakan bahwa Sistem Manajemen Rental PlayStation **Exito Playbox v1.0.0** secara resmi **DITERIMA** untuk digunakan dalam kegiatan operasional harian.

- **Pihak Klien:** Bpk. Hendra Gunawan (Owner Exito Playbox) — *Persetujuan Diberikan pada 5 Desember 2026*
- **Pihak Pengembang:** Maruf Syahbana (Full-Stack Developer) — *Diserahkan pada 5 Desember 2026*
