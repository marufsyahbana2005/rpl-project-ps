# Rencana User Acceptance Testing (UAT) — Exito Playbox (Lampiran B.4)

Dokumen ini memuat rencana pelaksanaan *User Acceptance Testing* (UAT) untuk memastikan bahwa Sistem Manajemen Rental PlayStation **Exito Playbox** (`rpl-project-ps`) memenuhi kebutuhan operasional pemilik dan kasir rental sebelum dirilis resmi (*production release* v1.0).

---

## 1. Tujuan Pengujian (Objectives)

1. Memvalidasi bahwa seluruh alur kerja operasional rental harian (mulai dari pembukaan sewa, pemilihan unit & paket, penghentian waktu sewa, hingga perhitungan denda) dapat digunakan dengan mudah dan benar oleh pengguna akhir (*end-users*).
2. Memverifikasi ketepatan batas hak akses antara kasir dan pemilik rental agar tidak terjadi kebocoran data rahasia atau salah wewenang.
3. Memperoleh persetujuan resmi (*acceptance sign-off*) dari pihak klien (Bpk. Hendra) sebagai syarat rilis akhir RTM-2.

---

## 2. Peserta Pengujian dari Pihak Klien

| Nama Peserta | Peran / Jabatan | Peran Pengujian dalam Sistem | Tanggung Jawab dalam UAT |
|---|---|---|---|
| **Bpk. Hendra Gunawan** | Pemilik Rental (*Owner*) | Pengguna Akun `owner` | Menguji modul kelola master unit konsol, penetapan tarif paket sewa, otorisasi hak akses, dan tinjauan laporan ringkasan transaksi. |
| **Rian Pratama** | Kasir Operasional Rental | Pengguna Akun `kasir` | Menguji alur pencatatan pelanggan baru, pemilihan unit konsol yang kosong, penghentian sewa saat pelanggan selesai bermain, dan verifikasi denda. |
| **Maruf Syahbana** | Pengembang / Fasilitator UAT | Pendamping Teknis | Memandu skenario uji, mencatat waktu dan kendala pengguna, serta mendokumentasikan masukan perbaikan. |

---

## 3. Lingkungan dan Data Uji Karangan

- **Perangkat Keras:** Laptop Lenovo ThinkPad / PC Kasir Exito Playbox (Layar resolusi $1920 \times 1080$, RAM 8 GB).
- **Peramban Web:** Google Chrome versi terbaru (Mode Incognito/Bersih).
- **Alamat URL Pengujian:** `http://localhost:5000` (Server lokal mandiri).
- **Basis Data Uji Karangan (`rental_uat.db`):**
  - **Akun Uji:**
    - Kasir: `kasir_siti` / Kata sandi: `KasirSiti#2026`
    - Pemilik: `owner_budi` / Kata sandi: `OwnerBudi#2026`
  - **Data Awal Unit Konsol:**
    - `PS4-01` (PlayStation 4, Status: Tersedia)
    - `PS4-02` (PlayStation 4, Status: Tersedia)
    - `PS5-01` (PlayStation 5, Status: Tersedia)
    - `PS5-02` (PlayStation 5, Status: Maintenance)
  - **Data Awal Paket Sewa:**
    - `Reguler 1 Jam PS4` (PS4, 60 Menit, Rp 10.000)
    - `Paket Puas 2 Jam PS4` (PS4, 120 Menit, Rp 18.000)
    - `Next-Gen 1 Jam PS5` (PS5, 60 Menit, Rp 15.000)
    - `Promo Khusus Mahasiswa` (PS4, 30 Menit, Rp 5.000)

---

## 4. Skenario Pengujian Alur Kerja Klien (Bahasa Awam Klien)

Skenario disusun menggunakan istilah operasional rental sehari-hari agar mudah dipahami oleh pemilik dan kasir tanpa beban istilah teknis pemrograman.

| ID Skenario | Kebutuhan Terkait | Judul Skenario Operasional | Langkah Pengujian Klien | Hasil yang Diharapkan oleh Klien | Kriteria Sukses Klien |
|:---:|:---:|---|---|---|:---:|
| **UAT-01** | **KF-01, 08** | Kasir masuk ke sistem dan mengecek konsol yang kosong | 1. Kasir membuka web rental.<br>2. Masukkan nama kasir dan kata sandi.<br>3. Klik tombol Masuk.<br>4. Perhatikan daftar konsol di halaman utama. | Kasir berhasil masuk ke sistem; muncul ucapan selamat datang; halaman menampilkan daftar konsol dengan tanda warna hijau (Tersedia) dan merah (Terpakai). | Kasir masuk $\le 3$ detik; status visual jelas terbaca. |
| **UAT-02** | **KF-01, 02** | Kasir mencatat pelanggan baru yang mulai bermain | 1. Klik menu **Buka Sewa**.<br>2. Ketik nama pelanggan *"Andi Wijaya"*.<br>3. Pilih konsol *"PS4-01"*.<br>4. Pilih paket *"Reguler 1 Jam PS4"*.<br>5. Klik tombol **Simpan Sewa**. | Data sewa tersimpan; muncul pesan hijau sewa berhasil dibuka; status konsol PS4-01 otomatis berubah jadi warna merah (Terpakai) dan tidak bisa dipilih orang lain. | Transaksi tersimpan rapi; unit langsung terkunci. |
| **UAT-03** | **KF-03, 07** | Kasir mengakhiri sesi sewa pelanggan yang tepat waktu | 1. Buka menu **Daftar Sewa**.<br>2. Cari nama pelanggan *"Andi Wijaya"*.<br>3. Klik tombol **Selesaikan Sewa** sebelum waktu habis.<br>4. Konfirmasi penyelesaian sewa. | Status sewa berubah menjadi 'Lunas'; denda tertulis Rp 0; unit PS4-01 otomatis kembali berstatus warna hijau (Tersedia) untuk disewa pelanggan berikutnya. | Konsol kembali kosong; denda Rp 0. |
| **UAT-04** | **KF-03, 07** | Kasir mengakhiri sewa pelanggan yang main lebih lama (kena denda) | 1. Buka transaksi pelanggan yang bermain melebihi batas waktu (misal lewat 20 menit).<br>2. Klik tombol **Selesaikan Sewa**.<br>3. Sistem otomatis menghitung kelebihan waktu di atas toleransi 5 menit. | Muncul rincian biaya denda keterlambatan (15 menit x Rp 1.000 = Rp 15.000); total tagihan terhitung otomatis; kasir mengonfirmasi pembayaran pelanggan. | Kasir tidak perlu menghitung denda manual dengan kalkulator. |
| **UAT-05** | **KF-01, 08** | Pemilik rental menambah unit konsol baru ke rental | 1. Keluar dari akun kasir $\rightarrow$ Masuk dengan akun Pemilik (*Owner*).<br>2. Klik menu **Kelola Master** $\rightarrow$ **Tambah Konsol**.<br>3. Masukkan kode konsol baru *"PS5-03"* dan jenis *"PS5"*.<br>4. Klik Simpan. | Unit konsol baru PS5-03 langsung terdaftar di sistem dengan status 'Tersedia' dan langsung siap disewakan oleh kasir. | Unit baru langsung muncul di kasir tanpa restart sistem. |
| **UAT-06** | **KNF-03** | Pemeriksaan batas wewenang kasir (keamanan uang & tarif) | 1. Kasir mencoba mengetik alamat URL khusus pemilik untuk mengubah tarif paket.<br>2. Kasir mencoba menghapus data unit konsol. | Sistem menampilkan peringatan penolakan akses (Akses Khusus Pemilik); kasir tidak dapat mengubah tarif sewa maupun menghapus aset rental. | Wewenang keuangan dan master data terlindungi aman dari kasir. |

---

## 5. Kriteria Penerimaan dan Kelulusan UAT (*Exit Criteria*)

Sistem dinyatakan **Lulus UAT dan Siap Rilis** apabila memenuhi seluruh parameter terukur berikut:
1. **Tingkat Kelulusan Skenario:** $100\%$ dari 6 skenario operasional di atas berstatus **LULUS** (dapat diselesaikan tanpa kendala kritis).
2. **Nol Cacat Kritis (*Zero Critical/High Severity Bugs*):** Tidak ada galat sistem yang menyebabkan halaman crash (HTTP 500), kalkulasi uang/denda salah, atau status konsol macet.
3. **Kepuasan Pengguna Akhir:** Klien (Bpk. Hendra) dan kasir (Rian Pratama) memberikan skor kemudahan penggunaan $\ge 4$ dari skala 5 pada lembar kuesioner akhir.
4. **Tanda Tangan Berita Acara:** Formulir berita acara serah terima UAT ditandatangani oleh Pemilik Rental dan Tim Pengembang.

---

## 6. Jadwal Pelaksanaan UAT (Sprint 3 — Minggu 14)

- **Hari / Tanggal:** Sabtu, 5 Desember 2026
- **Waktu:** Pukul 10.00 – 12.00 WIB (Durasi 120 Menit)
- **Tempat:** Gerai Rental Exito Playbox, Lantai 1 (Ruang Kasir & Operasional)
- **Rundown Acara UAT:**
  - `10:00 - 10:15`: Pembukaan, penjelasan singkat tujuan UAT, dan pembagian lembar skenario.
  - `10:15 - 10:45`: Simulasi pengujian mandiri oleh Kasir (Skenario UAT-01 s/d UAT-04).
  - `10:45 - 11:15`: Simulasi pengujian mandiri oleh Pemilik Rental (Skenario UAT-05 & UAT-06).
  - `11:15 - 11:45`: Uji coba bebas (*free exploratory session*) oleh klien dalam menangani pelanggan rental nyata.
  - `11:45 - 12:00`: Evaluasi masukan, pengisian lembar umpan balik, dan penandatanganan berita acara.

---

## 7. Prosedur Perekaman Temuan & Umpan Balik

1. Setiap kendala atau kebingungan pengguna selama pengujian dicatat langsung oleh fasilitator pada **Formulir Log Temuan UAT**:
   - Kolom: `ID Skenario`, `Waktu Kejadian`, `Komentar Verbal Pengguna`, `Klasifikasi (Cacat / Usulan Perubahan)`, dan `Tindakan Tindak Lanjut`.
2. Temuan yang bersifat menghambat alur kerja (*blocker*) akan langsung ditangani sebelum rilis v1.0, sedangkan saran estetika dicatat dalam backlog pengembangan rilis berikutnya (v1.1).
