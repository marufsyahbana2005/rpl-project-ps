# Bahan Paparan Presentasi Design Review (Langkah 10) — Exito Playbox

- **Waktu Paparan:** ± 5 Menit Presentasi + 5 Menit Tanya Jawab
- **Presenter / Pembicara:** Maruf Syahbana (Product Owner & Developer)
- **Artefak Acuan:** Repositori Git `rpl-project-ps`

---

## Slide 1: Gambaran Proyek dan Klien
- **Nama Proyek:** Exito Playbox Management System (Sistem Manajemen Rental PlayStation).
- **Profil Klien:** Bpk. Hendra, Pemilik & Operator Rental PS di Sampit (mengelola 8 unit konsol PlayStation: PS3, PS4, dan PS5).
- **Masalah Utama Klien:**
  1. Kesalahan pencatatan jam mulai sewa pada nota kertas manual saat jam sibuk.
  2. Sulitnya mengecek unit TV/PS mana yang kosong atau sedang berjalan dari meja kasir.
  3. Kerap keliru menghitung biaya denda kelebihan waktu (*overtime*) sehingga memicu komplain pelanggan.
  4. Pemilik kesulitan merekap omset harian tanpa menghitung ulang tumpukan nota fisik.
- **Solusi yang Dikembangkan:** Aplikasi web berbasis Python Flask dan SQLite dengan fitur *live timer*, dasbor ketersediaan visual via *HTTP polling*, kalkulasi denda otomatis ber-*grace period*, dan rekap omset instan.

---

## Slide 2: Peta Navigasi Sistem Antarmuka
- **Artefak:** [`docs/desain/wireframe/navigasi.png`](../wireframe/navigasi.png) | Kode: [`navigasi.mmd`](../wireframe/navigasi.mmd)
- **Poin Kunci Navigasi:**
  - Struktur berpusat pada **Dasbor Utama (Beranda)**.
  - Seluruh halaman operasional dapat dicapai maksimal dalam **1 hingga 2 klik** dari Beranda.
  - Tidak ada halaman yatim (*orphan page*); setiap halaman memiliki tombol kembali / menu navigasi global.
  - Terdapat pemisahan hak akses berbasis peran (*Role-Based Access Control*):
    - Halaman `wf-05` (Kelola Master) dan `wf-07` (Laporan Omset) **diberi label khusus Pemilik** dan dibatasi untuk peran *Owner*.

---

## Slide 3: Dua Wireframe Utama & Anotasi Penting

### 1. Dasbor Pemantauan Unit & Timer (`wf-02-dasbor-utama.png`)
- **Fungsi:** Pusat operasional kasir untuk memantau status seluruh unit konsol secara *real-time*.
- **Anotasi Kunci:**
  - Indikator warna status universal: Hijau (`Tersedia`), Merah (`Terpakai`), Kuning (`Overtime`), Abu-abu (`Maintenance`).
  - Unit `Tersedia` menampilkan tombol `[+] Mulai Sewa`.
  - Unit `Terpakai` menampilkan nama pelanggan, waktu mundur (*countdown*), dan tombol `[v] Selesaikan & Bayar`.
  - Banner sinkronisasi *polling* berkala (10 detik) untuk memberi tahu kasir kondisi pembaruan data otomatis.

### 2. Penghentian Sewa & Kelola Denda (`wf-04-selesai-sewa-denda.png`)
- **Fungsi:** Menyelesaikan transaksi kasir dengan transparansi biaya denda dan opsi pembatalan khusus.
- **Anotasi Kunci:**
  - Banner *Alert Overtime*: Muncul otomatis jika keterlambatan melewati ambang toleransi 5 menit (*grace period*).
  - Tabel rincian pemisahan biaya paket dan biaya denda per kelipatan 15/30 menit.
  - Tombol aksi: Hijau (`Konfirmasi Bayar Lunas`) dan Merah (`Batalkan Sewa - Kasus Mati Lampu`).

---

## Slide 4: Rencana Pengujian & Matriks Keterlacakan (Ringkas)
- **Artefak:** [`docs/pengujian/rencana-uji.md`](../../pengujian/rencana-uji.md)
- **Strategi Uji:** Manual Black-Box (Equivalence Partitioning & Boundary Value Analysis) + Uji Skema Database SQLite + UAT bersama pemilik.
- **Cakupan Matriks:**
  - Seluruh 4 kebutuhan fungsional *Must* (KF-01, KF-02, KF-04, KF-06) diverifikasi oleh test case terukur (TC-01 s/d TC-08).
  - Kebutuhan *Should* (KF-03, KF-07, KF-08) dan *Non-Fungsional* (KNF-01, KNF-03) diverifikasi oleh TC-05, TC-06, TC-09, TC-10, TC-11.
  - Terdapat 2 kasus tidak valid (TC-02 sewa unit terpakai, TC-09 nama kosong) dan 4 nilai batas (TC-03 durasi minimum 30 mnt, TC-04 promo Rp 0, TC-05 batas toleransi 5 mnt, TC-06 denda 6 mnt).

---

## Slide 5: Tiga Pertanyaan Kunci untuk Penelaah (Feedback Request)
1. **Pertanyaan 1 (Penanganan Denda & Grace Period):**  
   *"Apakah aturan toleransi keterlambatan 5 menit (grace period) sudah cukup jelas dan adil tergambar pada antarmuka kasir (`wf-04`), ataukah perlu ditambahkan penghitung waktu mundur toleransi langsung di kartu dasbor?"*
2. **Pertanyaan 2 (Keterbacaan Dasbor Jam Sibuk):**  
   *"Pada dasbor pemantauan unit (`wf-02`), apakah tata letak kartu konsol (grid 3 kolom) sudah cukup ergonomis bagi kasir yang harus melayani pelanggan cepat di jam sibuk rental?"*
3. **Pertanyaan 3 (Keamanan & Pemisahan Akses Laporan):**  
   *"Untuk menu Laporan Omset (`wf-07`), apakah pemisahan hak akses kasir vs owner melalui pembatasan rute dan penyembunyian menu sudah memenuhi standar keamanan pengujian antarmuka?"*
