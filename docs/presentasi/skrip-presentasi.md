# Skrip Presentasi Tugas Besar Rekayasa Perangkat Lunak
## Exito Playbox — PlayStation Rental Management System
**Total Alokasi Waktu: 20 Menit** (12 Menit Presentasi Konseptual + 5 Menit Live Demo + 3 Menit Refleksi & Penutup)

---

### [00:00 – 01:00] Slide 1: Pembukaan & Identitas Proyek
- **Aksi:** Tampilkan Slide 1. Berdiri tegap, kontak mata dengan dewan penguji.
- **Teks Lisan:**
  > "Selamat pagi/siang kepada Bapak/Ibu dosen penguji serta rekan-rekan sekalian. Terima kasih atas kesempatan yang diberikan pada hari ini. Perkenalkan, saya Maruf Syahbana, mewakili tim pengembang sistem Exito Playbox. Hari ini, saya akan mempresentasikan laporan akhir dan demonstrasi hasil pengembangan perangkat lunak bertajuk: *Sistem Informasi Manajemen Rental PlayStation Berbasis Web untuk Mitra Exito Playbox*. Sistem ini telah melalui siklus rekayasa perangkat lunak yang komprehensif mulai dari analisis kebutuhan, pemodelan arsitektur, pengerasan keamanan OWASP, pengujian otomatis, hingga tahap deployment produksi dengan status rilis versi 1.0.1. Mari kita mulai dengan melihat konteks permasalahan di lapangan."

---

### [01:00 – 02:30] Slide 2 & 3: Latar Belakang Masalah & Solusi yang Dibangun
- **Aksi:** Ganti ke Slide 2, lalu Slide 3.
- **Teks Lisan:**
  > "Exito Playbox merupakan mitra usaha rental PlayStation di Kota Sampit yang mengoperasikan 8 unit konsol PlayStation 3, 4, dan 5. Dari hasil investigasi awal kami, mitra menghadapi empat kendala operasional yang krusial. Pertama, pencatatan waktu sewa dilakukan manual di atas nota kertas sehingga sering terjadi kesalahan hitung saat jam sibuk. Kedua, kasir tidak memiliki visibilitas langsung mengenai ketersediaan unit tanpa harus memeriksa satu per satu ke setiap bilik. Ketiga, timbulnya perselisihan dengan pelanggan terkait perhitungan denda overtime yang tidak memiliki standar toleransi waktu yang pasti. Dan keempat, pemilik harus merekapitulasi nota fisik berjam-jam setiap malam untuk mengetahui omset harian.
  > Untuk menyelesaikan permasalahan tersebut, kami merancang sistem web responsif yang mengotomatisasi seluruh siklus sewa. Nilai tambah utama yang kami hadirkan adalah transaksi atomik multi-tabel: ketika kasir membuka atau menyelesaikan sewa, sistem menjamin konsistensi antara status unit fisik dan catatan finansial tanpa risiko inkonsistensi data."

---

### [02:30 – 04:30] Slide 4: Arsitektur Tiga Lapis (3-Tier) & Pemisahan Peran
- **Aksi:** Ganti ke Slide 4. Tunjukkan diagram arsitektur.
- **Teks Lisan:**
  > "Secara arsitektural, sistem dibangun dengan pola *Three-Tier Architecture*. Pada lapisan presentasi, kami menggunakan templat Jinja2 dengan fitur perenderan aman dan styling CSS responsif modern. Pada lapisan logika bisnis, kami memisahkan Controller di `app.py` dari Service Layer di `services.py`. Controller murni bertindak sebagai pengelola HTTP request, parsing input, dan pengembalian respons, sedangkan seluruh kalkulasi denda, validasi aturan bisnis, dan transaksi basis data diisolasi pada `services.py`. Pada lapisan persistensi data, kami menggunakan SQLite 3 dengan penegakan integritas relasional kunci asing. Sistem mengadopsi kontrol akses berbasis peran (RBAC) dengan dua entitas aktor: kasir untuk operasional transaksi sewa, dan pemilik atau owner yang memegang otorisasi penuh atas data master paket, harga, dan laporan pendapatan."

---

### [04:30 – 06:30] Slide 5 & 6: Pengerasan Keamanan Berbasis OWASP Top 10
- **Aksi:** Ganti ke Slide 5 secara singkat, lalu Slide 6.
- **Teks Lisan:**
  > "Aspek keamanan merupakan pilar fundamental dalam proyek ini. Kami tidak menganggap keamanan sebagai pelengkap di akhir, melainkan melakukan audit mandiri terstruktur terhadap 10 kategori risiko OWASP Top 10. Dari audit tersebut, kami mengidentifikasi dan memitigasi 7 potensi celah keamanan riil pada sistem. 
  > Pertama, untuk mencegah *Broken Access Control*, otorisasi tidak hanya dilakukan dengan menyembunyikan elemen tombol di HTML, melainkan ditegakkan dengan decorator backend `@peran_diperlukan`, serta mengamankan parameter pengalihan URL dari ancaman Open Redirect. Kedua, seluruh kata sandi diamankan menggunakan fungsi derivasi kunci modern `scrypt` dengan garam acak unik. Ketiga, seluruh kueri SQL menggunakan parameterisasi penuh dan karakter wildcard LIKE disanitasi dengan klausul `ESCAPE` untuk menutup risiko SQL Injection. Keempat, kami menyuntikkan security headers seperti `X-Frame-Options` untuk mencegah Clickjacking, memasang cookie flags `HttpOnly` dan `SameSite`, serta memasang modul proteksi CSRF berbasis sesi pada seluruh formulir POST dan rate limiter 5 kali percobaan login untuk mencegah serangan brute force."

---

### [06:30 – 08:30] Slide 7 & 8: Pengujian Otomatis, TDD Penutupan Cacat, & Evaluasi UAT
- **Aksi:** Ganti ke Slide 7, lalu Slide 8.
- **Teks Lisan:**
  > "Untuk memastikan kualitas kode, kami menerapkan strategi pengujian berlapis. Kami menyusun 22 kasus uji otomatis yang dieksekusi melalui framework Pytest, menghasilkan 38 skenario yang berstatus *passed* 100%. Kami juga menerapkan teknik pengujian mutasi manual untuk memverifikasi bahwa asersi uji benar-benar sensitif terhadap perubahan kode batas.
  > Selama pengujian, kami menemukan 3 cacat perangkat lunak yang berhasil diselesaikan melalui metode *Test-Driven Development* (TDD): Cacat D-01 terkait penanganan masukan non-string pada nama pelanggan, D-02 terkait validasi keunikan nama paket sewa secara case-insensitive, dan D-03 terkait perlindungan status konsol yang sedang disewa agar tidak dapat diubah ke status maintenance secara tidak sengaja.
  > Di sisi pengguna, kami melaksanakan User Acceptance Testing (UAT) langsung bersama Bpk. Hendra dan kasir rental. Seluruh 6 skenario operasional lulus 100%, dan pengukuran usabilitas menggunakan System Usability Scale (SUS) memperoleh skor rata-rata **87.5**, yang mengkategorikan sistem ini pada Grade A+ atau *Best Imaginable*."

---

### [08:30 – 10:00] Slide 9: Kesiapan Rilis & Deployment Produksi
- **Aksi:** Ganti ke Slide 9.
- **Teks Lisan:**
  > "Dari sisi rilis dan deployment, sistem mengikuti kaidah Semantic Versioning. Rilis perdana v1.0.0 diikuti hotfix v1.0.1 untuk penyempurnaan templat. Aplikasi siap dijalankan di lingkungan produksi menggunakan server WSGI multi-threaded **Waitress**, bukan server development bawaan Flask. Waitress dikonfigurasi dengan 6 worker threads yang mampu melayani antrean transaksi dengan response time rata-rata di bawah 50 milidetik. Integritas data rental diamankan oleh utilitas `cadangkan.py` yang memanfaatkan SQLite Online Backup API, memungkinkan pencadangan basis data secara *hot backup* tanpa perlu mematikan aplikasi kasir. Kami juga telah melengkapi repositori dengan README yang lolos uji pihak ketiga (*Stranger Test*) serta manual pengguna operasional yang ramah pengguna non-teknis."

---

### [10:00 – 15:00] Sesi Demonstrasi Sistem (Live Demo 5 Menit)
- **Aksi:** Buka peramban di http://127.0.0.1:8000 (atau port aktif) dan terminal.
- **Teks Lisan:**
  > "Sekarang, izinkan saya mendemonstrasikan sistem Exito Playbox secara langsung di lingkungan runner produksi Waitress."
  > 
  > *(Segmen 1: Demonstrasi Login & RBAC - 1 Menit)*
  > "Pertama, saya mencoba login sebagai kasir dengan kredensial salah. Perhatikan sistem menampilkan pesan kesalahan netral tanpa membocorkan apakah username atau password yang salah. Sekarang saya login dengan akun sah `kasir_andi`. Pada menu navigasi kasir, menu 'Kelola Master' dan laporan pemilik tidak dimunculkan. Apabila kasir mencoba mengakses rute `/packages` secara langsung lewat URL, server segera menolak dengan respons HTTP 403 Forbidden."
  >
  > *(Segmen 2: Pembukaan Sewa Transaksi Atomik - 1.5 Menit)*
  > "Kedua, kasir membuka transaksi sewa di rute `/sewa/buka`. Pada dropdown unit konsol, hanya unit yang berstatus 'tersedia' yang ditampilkan. Saya memilih unit `PS4-01`, memasukkan nama pelanggan 'Budi Santoso', dan memilih 'Paket Reguler 2 Jam'. Saat tombol 'Buka Sewa' diklik, sistem secara atomik mencatat baris transaksi baru dan seketika mengubah status inventaris unit `PS4-01` menjadi 'terpakai' dengan badge merah pada daftar unit."
  >
  > *(Segmen 3: Penyelesaian Sewa & Kalkulasi Denda Otomatis - 1.5 Menit)*
  > "Ketiga, mari kita lihat proses penyelesaian sewa. Saya memilih transaksi aktif. Sistem membandingkan waktu selesai riil terhadap paket. Apabila melewati batas durasi dengan toleransi di atas 5 menit, sistem secara otomatis menghitung denda keterlambatan Rp 1.000 per menit dan mencatatnya ke tabel `fines`. Setelah kasir mengonfirmasi pembayaran, unit `PS4-01` secara otomatis kembali berstatus 'tersedia' dan siap disewakan kepada pelanggan berikutnya."
  >
  > *(Segmen 4: Pengujian Cepat & Otomasi Cadangan - 1 Menit)*
  > "Terakhir, di terminal, saya mengeksekusi skrip `python tests/uji_cepat.py` untuk membuktikan bahwa seluruh 7 modul pengerasan keamanan dan integritas basis data berstatus LULUS dalam waktu kurang dari 2 detik. Kemudian saya mengeksekusi `python cadangkan.py` yang langsung menciptakan snapshot basis data terisolasi di folder cadangan tanpa mengganggu operasional sistem."

---

### [15:00 – 17:30] Slide 10: Analisis Praktik Vibe Coding & Kolaborasi AI
- **Aksi:** Kembali ke layar presentasi Slide 10.
- **Teks Lisan:**
  > "Selama proses pengembangan, kami mencatat setiap interaksi dengan kecerdasan buatan dalam jurnal *vibe coding* sebanyak 61 entri. Berdasarkan rekapitulasi skrip otomasi kami, proporsi keputusan adalah 90.2% Terima, 9.8% Ubah, dan 0% Tolak.
  > Dari 6 entri yang kami ubah, pelajaran paling berharga adalah: galat keamanan dan logika dari AI memiliki waktu diagnosis dan perbaikan terlama, rata-rata 25 menit per insiden. AI kerap menghasilkan kode yang tampak berjalan mulus di permukaan, tetapi memiliki kelemahan mendasar—seperti mengusulkan hashing SHA-256 tanpa garam atau membuat asersi uji otomatis yang terlalu longgar. Disiplin *human-in-the-loop* dan pengujian mutasi membuktikan bahwa peran pengembang manusia bergeser dari sekadar pengetik kode menjadi auditor arsitektur dan penjamin mutu perangkat lunak."

---

### [17:30 – 19:00] Slide 11 & 12: Keterbatasan, Saran, & Kesimpulan
- **Aksi:** Ganti ke Slide 11, lalu Slide 12.
- **Teks Lisan:**
  > "Tentu sistem ini masih memiliki ruang penyempurnaan. Kami mencatat tiga keterbatasan utama: modul rate limiter yang masih berbasis in-memory, mekanisme pembayaran yang belum terintegrasi dengan gateway QRIS otomatis, dan pencadangan yang masih tersimpan lokal di media fisik toko. Untuk pengembangan lanjutan, kami merekomendasikan migrasi basis data ke PostgreSQL terdistribusi dengan Redis cache, integrasi webhook payment gateway, dan kontainerisasi aplikasi menggunakan Docker.
  > Sebagai kesimpulan, proyek Exito Playbox telah berhasil memenuhi seluruh spesifikasi PRD, lolos audit keamanan OWASP, memperoleh pengakuan kepuasan pengguna Grade A+ pada uji UAT, dan terbukti siap beroperasi secara stabil di lingkungan produksi nyata."

---

### [19:00 – 20:00] Slide 13: Penutup & Tanya Jawab
- **Aksi:** Ganti ke Slide 13.
- **Teks Lisan:**
  > "Demikian pemaparan laporan akhir tugas besar rekayasa perangkat lunak sistem Exito Playbox. Terima kasih atas perhatian Bapak/Ibu dosen penguji. Waktu dan tempat saya kembalikan untuk sesi tanya jawab dan diskusi."
